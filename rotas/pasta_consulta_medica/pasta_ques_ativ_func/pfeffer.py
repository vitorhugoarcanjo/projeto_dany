from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from config.database import get_db_connection

bp_pfeffer = Blueprint('pfeffer', __name__)

@bp_pfeffer.route('/', methods=['GET', 'POST'])
def aplicar_pfeffer():
    if 'paciente_id' not in session:
        flash('Por favor, cadastre o paciente primeiro.', 'error')
        return redirect(url_for('cadastro.cadastro', proximo='pfeffer.aplicar_pfeffer'))

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
        # DADOS DO FORMULÁRIO PFEFFER
        dados_pfeffer = {
            # DADOS DA AVALIAÇÃO
            'data_avaliacao': request.form.get('data_avaliacao', ''),
            'informante': request.form.get('informante', ''),
            'parentesco': request.form.get('parentesco', ''),
            
            # QUESTÕES (0-3 pontos cada)
            'questao_1': request.form.get('questao_1', type=int),
            'questao_2': request.form.get('questao_2', type=int),
            'questao_3': request.form.get('questao_3', type=int),
            'questao_4': request.form.get('questao_4', type=int),
            'questao_5': request.form.get('questao_5', type=int),
            'questao_6': request.form.get('questao_6', type=int),
            'questao_7': request.form.get('questao_7', type=int),
            'questao_8': request.form.get('questao_8', type=int),
            'questao_9': request.form.get('questao_9', type=int),
            'questao_10': request.form.get('questao_10', type=int)
        }

        # CALCULA PONTUAÇÃO TOTAL
        pontuacao_total = calcular_pontuacao_pfeffer(dados_pfeffer)

        # INTERPRETAÇÃO DO RESULTADO
        if pontuacao_total <= 5:
            interpretacao = "Comprometimento funcional ausente ou mínimo"
            classificacao = "normal"
        elif pontuacao_total <= 10:
            interpretacao = "Comprometimento funcional leve"
            classificacao = "leve"
        elif pontuacao_total <= 20:
            interpretacao = "Comprometimento funcional moderado"
            classificacao = "moderado"
        else:
            interpretacao = "Comprometimento funcional grave"
            classificacao = "grave"

        # SALVA NO BANCO DE DADOS
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO aplicacoes_pfeffer 
            (paciente_id, informante, parentesco, dados_respostas, pontuacao_total, interpretacao, data_aplicacao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            paciente_id,
            dados_pfeffer['informante'],
            dados_pfeffer['parentesco'],
            str(dados_pfeffer), 
            pontuacao_total, 
            interpretacao,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        avaliacao_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # SALVA NA SESSÃO
        session['ultima_avaliacao_pfeffer'] = {
            'avaliacao_id': avaliacao_id,
            'pontuacao_total': pontuacao_total,
            'interpretacao': interpretacao,
            'classificacao': classificacao,
            'nome_paciente': paciente_info['nome'],
            'data_aplicacao': datetime.now().strftime('%d/%m/%Y %H:%M')
        }

        # LIMPA sessão
        session.pop('paciente_id', None)

        # REDIRECIONA PARA RESULTADO
        return redirect(url_for('pfeffer.resultado_pfeffer'))

    return render_template('pasta_consulta_medica/pasta_ques_ativ_func/pfeffer.html', 
                         paciente=paciente_info, 
                         data_atual=data_atual)

def calcular_pontuacao_pfeffer(dados):
    """Calcula a pontuação total do Questionário Pfeffer"""
    total = 0
    
    # Soma todas as questões (0-3 pontos cada)
    total += dados.get('questao_1', 0) or 0
    total += dados.get('questao_2', 0) or 0
    total += dados.get('questao_3', 0) or 0
    total += dados.get('questao_4', 0) or 0
    total += dados.get('questao_5', 0) or 0
    total += dados.get('questao_6', 0) or 0
    total += dados.get('questao_7', 0) or 0
    total += dados.get('questao_8', 0) or 0
    total += dados.get('questao_9', 0) or 0
    total += dados.get('questao_10', 0) or 0
    
    return total

@bp_pfeffer.route('/resultado')
def resultado_pfeffer():
    resultado = session.get('ultima_avaliacao_pfeffer', {})
    
    if not resultado:
        flash("Nenhuma avaliação Pfeffer encontrada. Por favor, realize uma avaliação primeiro.")
        return redirect(url_for('pfeffer.aplicar_pfeffer'))
    
    return render_template('pasta_consulta_medica/pasta_ques_ativ_func/resultado.html', resultado=resultado)