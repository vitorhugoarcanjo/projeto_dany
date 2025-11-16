from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from config.database import get_db_connection

bp_meem_g = Blueprint('meem_g', __name__)

@bp_meem_g.route('/', methods=['GET', 'POST'])
def aplicar_meem_g():
    if 'paciente_id' not in session:
        return redirect(url_for('cadastro.cadastro'))

    paciente_id = session['paciente_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, cpf, telefone, data_nascimento FROM pacientes WHERE id = ?", (paciente_id,))
    paciente = cursor.fetchone()
    conn.close()

    # ... O RESTO DO TEU CÓDIGO PERMANECE IGAL ...
    # Só troca todas as 'conn = sqlite3.connect(conexao_banco)' por 'conn = get_db_connection()'

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
    paciente = (paciente[0], paciente[1], paciente[2], data_formatada)

    if request.method == 'POST':
        # DADOS DO FORMULÁRIO
        dados_meem = {
            'nome_primeiro': request.form.get('nome_primeiro', type=int),
            'nome_ultimo': request.form.get('nome_ultimo', type=int),
            'data_nascimento': request.form.get('data_nascimento', type=int),
            'palavra_passaro': request.form.get('palavra_passaro', type=int),
            'palavra_casa': request.form.get('palavra_casa', type=int),
            'palavra_sombrinha': request.form.get('palavra_sombrinha', type=int),
            'instrucao_mao': request.form.get('instrucao_mao', type=int),
            'instrucao_olhos': request.form.get('instrucao_olhos', type=int),
            'nomeacao_caneta': request.form.get('nomeacao_caneta', type=int),
            'nomeacao_relogio': request.form.get('nomeacao_relogio', type=int),
            'nomeacao_sapato': request.form.get('nomeacao_sapato', type=int),
            'desenhe_circulo': request.form.get('desenhe_circulo', type=int),
            'copia_quadrado': request.form.get('copia_quadrado', type=int),
            'escrever_nome_primeiro': request.form.get('escrever_nome_primeiro', type=int),
            'escrever_nome_ultimo': request.form.get('escrever_nome_ultimo', type=int),
            'fluencia_animais': request.form.get('fluencia_animais', type=int),
            'soletrar_b': request.form.get('soletrar_b', type=int),
            'soletrar_o': request.form.get('soletrar_o', type=int),
            'soletrar_i': request.form.get('soletrar_i', type=int),
            # Campos de observação
            'obs_nome_primeiro': request.form.get('obs_nome_primeiro', ''),
            'obs_nome_ultimo': request.form.get('obs_nome_ultimo', ''),
            'obs_escrever_nome_primeiro': request.form.get('obs_escrever_nome_primeiro', ''),
            'obs_escrever_nome_ultimo': request.form.get('obs_escrever_nome_ultimo', ''),
        }

        # CALCULA PONTUAÇÃO TOTAL
        pontuacao_total = sum([
            dados_meem['nome_primeiro'] or 0,
            dados_meem['nome_ultimo'] or 0,
            dados_meem['data_nascimento'] or 0,
            dados_meem['palavra_passaro'] or 0,
            dados_meem['palavra_casa'] or 0,
            dados_meem['palavra_sombrinha'] or 0,
            dados_meem['instrucao_mao'] or 0,
            dados_meem['instrucao_olhos'] or 0,
            dados_meem['nomeacao_caneta'] or 0,
            dados_meem['nomeacao_relogio'] or 0,
            dados_meem['nomeacao_sapato'] or 0,
            dados_meem['desenhe_circulo'] or 0,
            dados_meem['copia_quadrado'] or 0,
            dados_meem['escrever_nome_primeiro'] or 0,
            dados_meem['escrever_nome_ultimo'] or 0,
            dados_meem['fluencia_animais'] or 0,
            dados_meem['soletrar_b'] or 0,
            dados_meem['soletrar_o'] or 0,
            dados_meem['soletrar_i'] or 0
        ])

        # INTERPRETAÇÃO DO RESULTADO
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

        # SALVA NO BANCO DE DADOS
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO aplicacoes_meem_g 
            (paciente_id, dados_respostas, pontuacao_total, interpretacao, data_aplicacao)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            paciente_id, 
            str(dados_meem), 
            pontuacao_total, 
            interpretacao,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        conn.close()

        # SALVA NA SESSÃO (se ainda quiser usar)
        atendimento = session.get('atendimento', {})
        atendimento['meem_g'] = {
            'dados': dados_meem,
            'pontuacao_total': pontuacao_total,
            'interpretacao': interpretacao,
            'classificacao': classificacao
        }
        session['atendimento'] = atendimento

        # REDIRECIONA PRA PÁGINA DE RESULTADO
        return redirect(url_for('meem_g.resultado_meem_g'))

    return render_template('pasta_consulta_medica/pasta_meen_g/pagina_1_meen_g.html', paciente=paciente)

@bp_meem_g.route('/resultado')
def resultado_meem_g():
    if 'paciente_id' not in session:
        return redirect(url_for('cadastro.cadastro'))
    
    # Pega os dados da sessão ou do banco
    resultado = session.get('atendimento', {}).get('meem_g', {})
    
    if not resultado:
        # Se não tiver na sessão, busca do banco
        paciente_id = session['paciente_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pontuacao_total, interpretacao, data_aplicacao 
            FROM aplicacoes_meem_g 
            WHERE paciente_id = ? 
            ORDER BY data_aplicacao DESC 
            LIMIT 1
        ''', (paciente_id,))
        
        ultimo_resultado = cursor.fetchone()
        conn.close()
        
        if ultimo_resultado:
            # DETERMINA A CLASSIFICAÇÃO BASEADA NA PONTUAÇÃO
            pontuacao = ultimo_resultado[0]
            if pontuacao >= 26:
                classificacao = "normal"
            elif pontuacao >= 18:
                classificacao = "leve"
            elif pontuacao >= 10:
                classificacao = "demencia_leve"
            else:
                classificacao = "demencia_grave"
                
            resultado = {
                'pontuacao_total': ultimo_resultado[0],
                'interpretacao': ultimo_resultado[1],
                'data_aplicacao': ultimo_resultado[2],
                'classificacao': classificacao
            }
    
    return render_template('pasta_consulta_medica/pasta_meen_g/resultado.html', resultado=resultado)

