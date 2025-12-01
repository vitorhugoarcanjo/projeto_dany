from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from config.database import get_db_connection

bp_relogio = Blueprint('relogio', __name__)

@bp_relogio.route('/', methods=['GET', 'POST'])
def aplicar_relogio():
    if 'paciente_id' not in session:
        flash('Por favor, cadastre o paciente primeiro.', 'error')
        return redirect(url_for('cadastro.cadastro', proximo='relogio.aplicar_relogio'))

    paciente_id = session['paciente_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, cpf, telefone, data_nascimento FROM pacientes WHERE id = ?", (paciente_id,))
    paciente = cursor.fetchone()
    conn.close()

    # Formatação da data de nascimento
    if paciente and paciente[3]:
        try:
            dt = datetime.strptime(paciente[3], '%Y-%m-%d')
            data_formatada = dt.strftime('%d/%m/%Y')
        except ValueError:
            data_formatada = paciente[3]
    else:
        data_formatada = ''

    paciente_info = {
        'nome': paciente[0],
        'cpf': paciente[1],
        'telefone': paciente[2],
        'data_nascimento': data_formatada
    }

    data_atual = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST':
        # DADOS DO FORMULÁRIO RELÓGIO
        dados_relogio = {
            # DADOS DA AVALIAÇÃO
            'data_avaliacao': request.form.get('data_avaliacao', ''),
            
            # PONTUAÇÃO (1-10 pontos)
            'pontuacao': request.form.get('pontuacao', type=int),
            
            # COMENTÁRIOS
            'comentarios': request.form.get('comentarios', '')
        }

        # INTERPRETAÇÃO DO RESULTADO
        pontuacao = dados_relogio['pontuacao'] or 0
        interpretacao = obter_interpretacao_relogio(pontuacao)
        classificacao = obter_classificacao_relogio(pontuacao)

        # SALVA NO BANCO DE DADOS
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO aplicacoes_relogio 
            (paciente_id, dados_respostas, pontuacao_total, interpretacao, data_aplicacao)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            paciente_id,
            str(dados_relogio), 
            pontuacao, 
            interpretacao,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        avaliacao_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # SALVA NA SESSÃO
        session['ultima_avaliacao_relogio'] = {
            'avaliacao_id': avaliacao_id,
            'pontuacao_total': pontuacao,
            'interpretacao': interpretacao,
            'classificacao': classificacao,
            'nome_paciente': paciente_info['nome'],
            'data_aplicacao': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'comentarios': dados_relogio['comentarios']
        }

        # LIMPA sessão
        session.pop('paciente_id', None)

        # REDIRECIONA PARA RESULTADO
        return redirect(url_for('relogio.resultado_relogio'))

    return render_template('pasta_consulta_medica/pasta_desen_relogio/desenho_relogio.html', 
                         paciente=paciente_info, 
                         data_atual=data_atual)

def obter_interpretacao_relogio(pontuacao):
    """Retorna a interpretação baseada na pontuação do relógio"""
    if pontuacao >= 10:
        return "Relógio e números estão corretos"
    elif pontuacao >= 6:
        return "Relógio e números estão corretos com pequenas imperfeições"
    elif pontuacao >= 5:
        return "Desenhos do relógio e dos números incorretos"
    elif pontuacao >= 1:
        return "Comprometimento significativo na representação do relógio"
    else:
        return "Não tentou ou não conseguiu representar um relógio"

def obter_classificacao_relogio(pontuacao):
    """Retorna a classificação baseada na pontuação"""
    if pontuacao >= 9:
        return "excelente"
    elif pontuacao >= 7:
        return "bom"
    elif pontuacao >= 5:
        return "regular"
    elif pontuacao >= 3:
        return "ruim"
    else:
        return "muito_ruim"

@bp_relogio.route('/resultado')
def resultado_relogio():
    resultado = session.get('ultima_avaliacao_relogio', {})
    
    if not resultado:
        flash("Nenhuma avaliação do Relógio encontrada. Por favor, realize uma avaliação primeiro.")
        return redirect(url_for('relogio.aplicar_relogio'))
    
    return render_template('pasta_consulta_medica/pasta_desen_relogio/resultado.html', resultado=resultado)