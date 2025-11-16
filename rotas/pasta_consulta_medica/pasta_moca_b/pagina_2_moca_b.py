from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from config.database import get_db_connection

bp_moca_b = Blueprint('moca_b', __name__)

@bp_moca_b.route('/', methods=['GET', 'POST'])
def aplicar_moca_b():
    if 'paciente_id' not in session:
        return redirect(url_for('cadastro.cadastro'))

    paciente_id = session['paciente_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, cpf, telefone, data_nascimento FROM pacientes WHERE id = ?", (paciente_id,))
    paciente = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        # DADOS DO FORMULÁRIO MoCA-B (VERSÃO CORRIGIDA)
        dados_moca = {
            # FUNÇÕES EXECUTIVAS - TESTE DE TRILHAS (1 ponto)
            'funcoes_executivas_trilhas': request.form.get('funcoes_executivas_trilhas', type=int) or 0,
            'horario_inicio': request.form.get('horario_inicio', ''),
            
            # EVOCAÇÃO IMEDIATA (5 palavras - 2 tentativas) - NENHUM PONTO SEGUNDO INSTRUÇÕES
            'evocacao_tomate_t1': request.form.get('evocacao_tomate_t1', type=int) or 0,
            'evocacao_sofa_t1': request.form.get('evocacao_sofa_t1', type=int) or 0,
            'evocacao_joelho_t1': request.form.get('evocacao_joelho_t1', type=int) or 0,
            'evocacao_azul_t1': request.form.get('evocacao_azul_t1', type=int) or 0,
            'evocacao_colher_t1': request.form.get('evocacao_colher_t1', type=int) or 0,
            'evocacao_tomate_t2': request.form.get('evocacao_tomate_t2', type=int) or 0,
            'evocacao_sofa_t2': request.form.get('evocacao_sofa_t2', type=int) or 0,
            'evocacao_joelho_t2': request.form.get('evocacao_joelho_t2', type=int) or 0,
            'evocacao_azul_t2': request.form.get('evocacao_azul_t2', type=int) or 0,
            'evocacao_colher_t2': request.form.get('evocacao_colher_t2', type=int) or 0,
            
            # FLUÊNCIA (frutas em 1 minuto)
            'fluencia_frutas': request.form.get('fluencia_frutas', type=int) or 0,
            
            # ORIENTAÇÃO (6 itens)
            'orientacao_horario': request.form.get('orientacao_horario', type=int) or 0,
            'orientacao_dia_semana': request.form.get('orientacao_dia_semana', type=int) or 0,
            'orientacao_mes': request.form.get('orientacao_mes', type=int) or 0,
            'orientacao_ano': request.form.get('orientacao_ano', type=int) or 0,
            'orientacao_local': request.form.get('orientacao_local', type=int) or 0,
            'orientacao_cidade': request.form.get('orientacao_cidade', type=int) or 0,
            
            # CÁLCULO (3 formas de pagar R$13)
            'calculo_forma1': request.form.get('calculo_forma1', type=int) or 0,
            'calculo_forma2': request.form.get('calculo_forma2', type=int) or 0,
            'calculo_forma3': request.form.get('calculo_forma3', type=int) or 0,
            
            # ABSTRAÇÃO (3 categorias)
            'abstracao_trem_barco': request.form.get('abstracao_trem_barco', type=int) or 0,
            'abstracao_norte_sul': request.form.get('abstracao_norte_sul', type=int) or 0,
            'abstracao_tambor_flauta': request.form.get('abstracao_tambor_flauta', type=int) or 0,
            
            # EVOCAÇÃO TARDIA (5 palavras)
            'evocacao_tardia_tomate': request.form.get('evocacao_tardia_tomate', type=int) or 0,
            'evocacao_tardia_sofa': request.form.get('evocacao_tardia_sofa', type=int) or 0,
            'evocacao_tardia_joelho': request.form.get('evocacao_tardia_joelho', type=int) or 0,
            'evocacao_tardia_azul': request.form.get('evocacao_tardia_azul', type=int) or 0,
            'evocacao_tardia_colher': request.form.get('evocacao_tardia_colher', type=int) or 0,
            
            # PERCEPÇÃO VISUAL (10 figuras)
            'percepcao_tesoura': request.form.get('percepcao_tesoura', type=int) or 0,
            'percepcao_camiseta': request.form.get('percepcao_camiseta', type=int) or 0,
            'percepcao_banana': request.form.get('percepcao_banana', type=int) or 0,
            'percepcao_abajur': request.form.get('percepcao_abajur', type=int) or 0,
            'percepcao_vela': request.form.get('percepcao_vela', type=int) or 0,
            'percepcao_relogio': request.form.get('percepcao_relogio', type=int) or 0,
            'percepcao_xicara': request.form.get('percepcao_xicara', type=int) or 0,
            'percepcao_folha': request.form.get('percepcao_folha', type=int) or 0,
            'percepcao_chave': request.form.get('percepcao_chave', type=int) or 0,
            'percepcao_colher': request.form.get('percepcao_colher', type=int) or 0,
            
            # NOMEAÇÃO (4 animais)
            'nomeacao_zebra': request.form.get('nomeacao_zebra', type=int) or 0,
            'nomeacao_pavao': request.form.get('nomeacao_pavao', type=int) or 0,
            'nomeacao_tigre': request.form.get('nomeacao_tigre', type=int) or 0,
            'nomeacao_borboleta': request.form.get('nomeacao_borboleta', type=int) or 0,
            
            # ATENÇÃO
            'atencao_circulos_erros': request.form.get('atencao_circulos_erros', type=int) or 0,
            'atencao_circulos_quadrados_erros': request.form.get('atencao_circulos_quadrados_erros', type=int) or 0,
            
            # DADOS ADICIONAIS
            'horario_final': request.form.get('horario_final', ''),
            'escolaridade_anos': request.form.get('escolaridade_anos', type=int) or 0,
            'anal_fabeto': request.form.get('anal_fabeto', type=int) or 0,
        }

        # CALCULA PONTUAÇÃO TOTAL (VERSÃO CORRIGIDA)
        pontuacao_total = calcular_pontuacao_moca_b_corrigida(dados_moca)
        
        # INTERPRETAÇÃO
        interpretacao = interpretar_moca_b(pontuacao_total)

        # SALVA NO BANCO
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO aplicacoes_moca_b 
            (paciente_id, dados_respostas, pontuacao_total, interpretacao, data_aplicacao)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            paciente_id, 
            str(dados_moca), 
            pontuacao_total, 
            interpretacao,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        conn.close()

        # SALVA NA SESSÃO
        atendimento = session.get('atendimento', {})
        atendimento['moca_b'] = {
            'dados': dados_moca,
            'pontuacao_total': pontuacao_total,
            'interpretacao': interpretacao
        }
        session['atendimento'] = atendimento

        return redirect(url_for('moca_b.resultado_moca_b'))

    return render_template('pasta_consulta_medica/pasta_moca_b/pagina_2_moca_b.html', paciente=paciente)

def calcular_pontuacao_moca_b_corrigida(dados):
    """Calcula a pontuação total do MoCA-B CONFORME INSTRUÇÕES OFICIAIS"""
    pontuacao = 0
    
    # 1. FUNÇÕES EXECUTIVAS - TESTE DE TRILHAS (1 ponto)
    pontuacao += dados['funcoes_executivas_trilhas']
    
    # 2. EVOCAÇÃO IMEDIATA - NENHUM PONTO (conforme instruções)
    # Não soma pontos - só serve para a evocação tardia
    
    # 3. FLUÊNCIA (frutas)
    frutas = dados['fluencia_frutas']
    if frutas >= 13:
        pontuacao += 2
    elif frutas >= 8:
        pontuacao += 1
    # 7 ou menos = 0 pontos
    
    # 4. ORIENTAÇÃO (6 pontos)
    pontuacao += sum([dados['orientacao_horario'], dados['orientacao_dia_semana'],
                     dados['orientacao_mes'], dados['orientacao_ano'],
                     dados['orientacao_local'], dados['orientacao_cidade']])
    
    # 5. CÁLCULO (3 pontos)
    pontuacao += sum([dados['calculo_forma1'], dados['calculo_forma2'], dados['calculo_forma3']])
    
    # 6. ABSTRAÇÃO (3 pontos)
    pontuacao += sum([dados['abstracao_trem_barco'], dados['abstracao_norte_sul'], dados['abstracao_tambor_flauta']])
    
    # 7. EVOCAÇÃO TARDIA (5 pontos) - SÓ EVOCAÇÃO LIVRE
    pontuacao += sum([dados['evocacao_tardia_tomate'], dados['evocacao_tardia_sofa'],
                     dados['evocacao_tardia_joelho'], dados['evocacao_tardia_azul'],
                     dados['evocacao_tardia_colher']])
    
    # 8. PERCEPÇÃO VISUAL (10 figuras) - CORRIGIDO
    percepcao = sum([dados['percepcao_tesoura'], dados['percepcao_camiseta'], dados['percepcao_banana'],
                    dados['percepcao_abajur'], dados['percepcao_vela'], dados['percepcao_relogio'],
                    dados['percepcao_xicara'], dados['percepcao_folha'], dados['percepcao_chave'],
                    dados['percepcao_colher']])
    if percepcao >= 9:
        pontuacao += 3
    elif percepcao >= 6:
        pontuacao += 2
    elif percepcao >= 4:  # CORRIGIDO: 4-5 objetos = 1 ponto
        pontuacao += 1
    # 3 ou menos = 0 pontos
    
    # 9. NOMEAÇÃO (4 pontos)
    pontuacao += sum([dados['nomeacao_zebra'], dados['nomeacao_pavao'], 
                     dados['nomeacao_tigre'], dados['nomeacao_borboleta']])
    
    # 10. ATENÇÃO
    # Primeira tarefa (círculos)
    if dados['atencao_circulos_erros'] <= 1:  # CORRIGIDO: no máximo 1 erro
        pontuacao += 1
    
    # Segunda tarefa (círculos e quadrados)
    erros_circulos_quadrados = dados['atencao_circulos_quadrados_erros']
    if erros_circulos_quadrados <= 2:
        pontuacao += 2
    elif erros_circulos_quadrados == 3:
        pontuacao += 1
    # 4 ou mais erros = 0 pontos
    
    # BÔNUS POR ESCOLARIDADE (APENAS SE PONTUAÇÃO < 30)
    if pontuacao < 30:
        if dados['escolaridade_anos'] < 4:
            pontuacao += 1
        if dados['anal_fabeto'] and pontuacao < 30:
            pontuacao += 1
    
    return min(pontuacao, 30)  # Máximo 30 pontos

def interpretar_moca_b(pontuacao):
    """Interpreta a pontuação do MoCA-B"""
    if pontuacao >= 26:
        return "Cognição normal"
    elif pontuacao >= 18:
        return "Comprometimento cognitivo leve"
    elif pontuacao >= 10:
        return "Demência leve"
    else:
        return "Demência moderada/grave"

@bp_moca_b.route('/resultado')
def resultado_moca_b():
    if 'paciente_id' not in session:
        return redirect(url_for('cadastro.cadastro'))
    
    resultado = session.get('atendimento', {}).get('moca_b', {})
    
    if not resultado:
        paciente_id = session['paciente_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pontuacao_total, interpretacao, data_aplicacao 
            FROM aplicacoes_moca_b 
            WHERE paciente_id = ? 
            ORDER BY data_aplicacao DESC 
            LIMIT 1
        ''', (paciente_id,))
        
        ultimo_resultado = cursor.fetchone()
        conn.close()
        
        if ultimo_resultado:
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
                'pontuacao_total': pontuacao,
                'interpretacao': ultimo_resultado[1],
                'data_aplicacao': ultimo_resultado[2],
                'classificacao': classificacao
            }
    
    return render_template('pasta_consulta_medica/pasta_moca_b/resultado.html', resultado=resultado)