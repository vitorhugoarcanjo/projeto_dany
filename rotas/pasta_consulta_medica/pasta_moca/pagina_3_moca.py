from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from config.database import get_db_connection

bp_moca = Blueprint('moca', __name__)

@bp_moca.route('/', methods=['GET', 'POST'])
def aplicar_moca():
    # VERIFICA SE TEM PACIENTE NA SESSÃO (vindo do cadastro)
    if 'paciente_id' not in session:
        flash('Por favor, cadastre o paciente primeiro.', 'error')
        return redirect(url_for('cadastro.cadastro', proximo='moca.aplicar_moca'))

    paciente_id = session['paciente_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, cpf, telefone, data_nascimento FROM pacientes WHERE id = ?", (paciente_id,))
    paciente = cursor.fetchone()
    conn.close()

    if not paciente:
        flash('Paciente não encontrado.', 'error')
        return redirect(url_for('cadastro.cadastro', proximo='moca.aplicar_moca'))

    # Formatação da data de nascimento
    if paciente and paciente[3]:
        try:
            dt = datetime.strptime(paciente[3], '%Y-%m-%d')
            data_formatada = dt.strftime('%d/%m/%Y')
        except ValueError:
            data_formatada = paciente[3]
    else:
        data_formatada = ''

    # Ajusta a tupla paciente com data formatada
    paciente_info = {
        'nome': paciente[0],
        'cpf': paciente[1],
        'telefone': paciente[2],
        'data_nascimento': data_formatada
    }

    # Data atual para o template
    data_atual = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST':
        # DADOS DO FORMULÁRIO MOCA
        dados_moca = {
            # DADOS ADICIONAIS DA AVALIAÇÃO
            'escolaridade': request.form.get('escolaridade', ''),
            'data_avaliacao': request.form.get('data_avaliacao', ''),
            
            # VISUOSPACIAL/EXECUTIVA
            'trilha_pontos': request.form.get('trilha_pontos', type=int),
            'cubo_pontos': request.form.get('cubo_pontos', type=int),
            'relogio_contorno': request.form.get('relogio_contorno', type=int),
            'relogio_numeros': request.form.get('relogio_numeros', type=int),
            'relogio_ponteiros': request.form.get('relogio_ponteiros', type=int),
            
            # NOMEAÇÃO
            'camelo': request.form.get('camelo', type=int),
            'leao': request.form.get('leao', type=int),
            'rinoceronte': request.form.get('rinoceronte', type=int),
            
            # MEMÓRIA (evocação tardia)
            'memoria_rosto': request.form.get('memoria_rosto', type=int),
            'memoria_veludo': request.form.get('memoria_veludo', type=int),
            'memoria_igreja': request.form.get('memoria_igreja', type=int),
            'memoria_margarida': request.form.get('memoria_margarida', type=int),
            'memoria_vermelho': request.form.get('memoria_vermelho', type=int),
            
            # ATENÇÃO
            'digitos_direta': request.form.get('digitos_direta', type=int),
            'digitos_inversa': request.form.get('digitos_inversa', type=int),
            'vigilancia': request.form.get('vigilancia', type=int),
            'subtracao_93': request.form.get('subtracao_93', type=int),
            'subtracao_86': request.form.get('subtracao_86', type=int),
            'subtracao_79': request.form.get('subtracao_79', type=int),
            'subtracao_72': request.form.get('subtracao_72', type=int),
            'subtracao_65': request.form.get('subtracao_65', type=int),
            
            # LINGUAGEM
            'sentenca_1': request.form.get('sentenca_1', type=int),
            'sentenca_2': request.form.get('sentenca_2', type=int),
            'fluencia_verbal': request.form.get('fluencia_verbal', type=int),
            
            # ABSTRAÇÃO
            'abstracao_trem': request.form.get('abstracao_trem', type=int),
            'abstracao_relogio': request.form.get('abstracao_relogio', type=int),
            
            # ORIENTAÇÃO
            'orientacao_dia': request.form.get('orientacao_dia', type=int),
            'orientacao_mes': request.form.get('orientacao_mes', type=int),
            'orientacao_ano': request.form.get('orientacao_ano', type=int),
            'orientacao_dia_semana': request.form.get('orientacao_dia_semana', type=int),
            'orientacao_lugar': request.form.get('orientacao_lugar', type=int),
            'orientacao_cidade': request.form.get('orientacao_cidade', type=int)
        }

        # CALCULA PONTUAÇÃO TOTAL DO MOCA
        pontuacao_total = calcular_pontuacao_moca(dados_moca)

        # INTERPRETAÇÃO DO RESULTADO (MOCA)
        if pontuacao_total >= 26:
            interpretacao = "Cognição normal"
            classificacao = "normal"
        elif pontuacao_total >= 18:
            interpretacao = "Comprometimento cognitivo leve"
            classificacao = "leve"  
        elif pontuacao_total >= 10:
            interpretacao = "Demência leve"
            classificacao = "demencia_leve"
        else:
            interpretacao = "Demência moderada/grave"
            classificacao = "demencia_grave"

        # SALVA NO BANCO DE DADOS (COM paciente_id)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO aplicacoes_moca 
            (paciente_id, escolaridade, dados_respostas, pontuacao_total, interpretacao, data_aplicacao)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            paciente_id,
            dados_moca['escolaridade'],
            str(dados_moca), 
            pontuacao_total, 
            interpretacao,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        # Pega o ID da avaliação recém-criada
        avaliacao_id = cursor.lastrowid
        
        conn.commit()
        conn.close()

        # SALVA NA SESSÃO APENAS OS DADOS DESSA AVALIAÇÃO ESPECÍFICA
        session['ultima_avaliacao_moca'] = {
            'avaliacao_id': avaliacao_id,
            'pontuacao_total': pontuacao_total,
            'interpretacao': interpretacao,
            'classificacao': classificacao,
            'nome_paciente': paciente_info['nome'],
            'data_aplicacao': datetime.now().strftime('%d/%m/%Y %H:%M')
        }

        # LIMPA o paciente_id da sessão para evitar conflitos
        session.pop('paciente_id', None)

        # REDIRECIONA PRA PÁGINA DE RESULTADO
        return redirect(url_for('moca.resultado_moca'))

    return render_template('pasta_consulta_medica/pasta_moca/pagina_moca.html', 
                         paciente=paciente_info, 
                         data_atual=data_atual)

def calcular_pontuacao_moca(dados):
    """Calcula a pontuação total do MoCA seguindo as regras oficiais"""
    total = 0
    
    # VISUOSPACIAL/EXECUTIVA (máx 5 pontos)
    total += dados.get('trilha_pontos', 0) or 0
    total += dados.get('cubo_pontos', 0) or 0
    total += dados.get('relogio_contorno', 0) or 0
    total += dados.get('relogio_numeros', 0) or 0
    total += dados.get('relogio_ponteiros', 0) or 0
    
    # NOMEAÇÃO (máx 3 pontos)
    total += dados.get('camelo', 0) or 0
    total += dados.get('leao', 0) or 0
    total += dados.get('rinoceronte', 0) or 0
    
    # MEMÓRIA - evocação tardia (máx 5 pontos)
    total += dados.get('memoria_rosto', 0) or 0
    total += dados.get('memoria_veludo', 0) or 0
    total += dados.get('memoria_igreja', 0) or 0
    total += dados.get('memoria_margarida', 0) or 0
    total += dados.get('memoria_vermelho', 0) or 0
    
    # ATENÇÃO (máx 6 pontos)
    total += dados.get('digitos_direta', 0) or 0
    total += dados.get('digitos_inversa', 0) or 0
    total += dados.get('vigilancia', 0) or 0
    
    # Subtração seriada (0-3 pontos)
    subtracoes = [
        dados.get('subtracao_93'),
        dados.get('subtracao_86'), 
        dados.get('subtracao_79'),
        dados.get('subtracao_72'),
        dados.get('subtracao_65')
    ]
    corretas = sum(1 for s in subtracoes if s == 1)
    if corretas >= 4:
        total += 3
    elif corretas >= 2:
        total += 2
    elif corretas >= 1:
        total += 1
    
    # LINGUAGEM (máx 3 pontos)
    total += dados.get('sentenca_1', 0) or 0
    total += dados.get('sentenca_2', 0) or 0
    total += dados.get('fluencia_verbal', 0) or 0
    
    # ABSTRAÇÃO (máx 2 pontos)
    total += dados.get('abstracao_trem', 0) or 0
    total += dados.get('abstracao_relogio', 0) or 0
    
    # ORIENTAÇÃO (máx 6 pontos)
    total += dados.get('orientacao_dia', 0) or 0
    total += dados.get('orientacao_mes', 0) or 0
    total += dados.get('orientacao_ano', 0) or 0
    total += dados.get('orientacao_dia_semana', 0) or 0
    total += dados.get('orientacao_lugar', 0) or 0
    total += dados.get('orientacao_cidade', 0) or 0
    
    # AJUSTE PARA ESCOLARIDADE (≤12 anos = +1 ponto)
    escolaridade = dados.get('escolaridade', '')
    try:
        if escolaridade and int(escolaridade) <= 12:
            total += 1
    except (ValueError, TypeError):
        pass
    
    return total

@bp_moca.route('/resultado')
def resultado_moca():
    # Busca apenas a última avaliação do MoCA dessa sessão específica
    resultado = session.get('ultima_avaliacao_moca', {})
    
    if not resultado:
        # Se não tiver na sessão, mostra mensagem
        flash("Nenhuma avaliação MoCA encontrada. Por favor, realize uma avaliação primeiro.")
        return redirect(url_for('moca.aplicar_moca'))
    
    return render_template('pasta_consulta_medica/pasta_moca/resultado.html', resultado=resultado)