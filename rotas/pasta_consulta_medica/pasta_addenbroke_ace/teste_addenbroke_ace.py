from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from config.database import get_db_connection

bp_acer = Blueprint('acer', __name__)

@bp_acer.route('/', methods=['GET', 'POST'])
def aplicar_acer():
    if 'paciente_id' not in session:
        flash('Por favor, cadastre o paciente primeiro.', 'error')
        return redirect(url_for('cadastro.cadastro', proximo='acer.aplicar_acer'))

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
        # DADOS DO FORMULÁRIO ACE-R
        dados_acer = {
            # DADOS DA AVALIAÇÃO
            'data_avaliacao': request.form.get('data_avaliacao', ''),
            'hospital': request.form.get('hospital', ''),
            'examinador': request.form.get('examinador', ''),
            'escolaridade': request.form.get('escolaridade', ''),
            'profissao': request.form.get('profissao', ''),
            'dominancia_manual': request.form.get('dominancia_manual', ''),
            
            # ORIENTAÇÃO (0-10 pontos)
            'orientacao_dia_semana': request.form.get('orientacao_dia_semana', type=int),
            'orientacao_dia_mes': request.form.get('orientacao_dia_mes', type=int),
            'orientacao_mes': request.form.get('orientacao_mes', type=int),
            'orientacao_ano': request.form.get('orientacao_ano', type=int),
            'orientacao_hora': request.form.get('orientacao_hora', type=int),
            'orientacao_local_especifico': request.form.get('orientacao_local_especifico', type=int),
            'orientacao_local_generico': request.form.get('orientacao_local_generico', type=int),
            'orientacao_bairro': request.form.get('orientacao_bairro', type=int),
            'orientacao_cidade': request.form.get('orientacao_cidade', type=int),
            'orientacao_estado': request.form.get('orientacao_estado', type=int),
            
            # REGISTRO (0-3 pontos)
            'registro_carro': request.form.get('registro_carro', type=int),
            'registro_vaso': request.form.get('registro_vaso', type=int),
            'registro_tijolo': request.form.get('registro_tijolo', type=int),
            'tentativas_registro': request.form.get('tentativas_registro', type=int),
            
            # ATENÇÃO & CONCENTRAÇÃO (0-5 pontos)
            'subtracao_93': request.form.get('subtracao_93', type=int),
            'subtracao_86': request.form.get('subtracao_86', type=int),
            'subtracao_79': request.form.get('subtracao_79', type=int),
            'subtracao_72': request.form.get('subtracao_72', type=int),
            'subtracao_65': request.form.get('subtracao_65', type=int),
            
            # MEMÓRIA - Recordação (0-3 pontos)
            'memoria_carro': request.form.get('memoria_carro', type=int),
            'memoria_vaso': request.form.get('memoria_vaso', type=int),
            'memoria_tijolo': request.form.get('memoria_tijolo', type=int),
            
            # MEMÓRIA - Memória anterógrada (0-7 pontos)
            'memoria_renato_t3': request.form.get('memoria_renato_t3', type=int),
            'memoria_rua_t3': request.form.get('memoria_rua_t3', type=int),
            'memoria_73_t3': request.form.get('memoria_73_t3', type=int),
            'memoria_santarem_t3': request.form.get('memoria_santarem_t3', type=int),
            'memoria_para_t3': request.form.get('memoria_para_t3', type=int),
            
            # MEMÓRIA - Memória retrógrada (0-4 pontos)
            'memoria_presidente_atual': request.form.get('memoria_presidente_atual', type=int),
            'memoria_presidente_brasilia': request.form.get('memoria_presidente_brasilia', type=int),
            'memoria_presidente_eua': request.form.get('memoria_presidente_eua', type=int),
            'memoria_presidente_eua_assassinado': request.form.get('memoria_presidente_eua_assassinado', type=int),
            
            # FLUÊNCIA VERBAL - Letra P (0-7 pontos)
            'fluencia_p_pontos': request.form.get('fluencia_p_pontos', type=int),
            'fluencia_p_total': request.form.get('fluencia_p_total', type=int),
            
            # FLUÊNCIA VERBAL - Animais (0-7 pontos)
            'fluencia_animais_pontos': request.form.get('fluencia_animais_pontos', type=int),
            'fluencia_animais_total': request.form.get('fluencia_animais_total', type=int),
            
            # LINGUAGEM - Compreensão (0-4 pontos)
            'linguagem_fechar_olhos': request.form.get('linguagem_fechar_olhos', type=int),
            'linguagem_pegar_papel': request.form.get('linguagem_pegar_papel', type=int),
            'linguagem_dobrar_papel': request.form.get('linguagem_dobrar_papel', type=int),
            'linguagem_colocar_chao': request.form.get('linguagem_colocar_chao', type=int),
            
            # LINGUAGEM - Escrita (0-1 ponto)
            'linguagem_escrita': request.form.get('linguagem_escrita', type=int),
            
            # LINGUAGEM - Repetição (0-4 pontos)
            'linguagem_repeticao_palavras': request.form.get('linguagem_repeticao_palavras', type=int),
            'linguagem_repeticao_acima': request.form.get('linguagem_repeticao_acima', type=int),
            'linguagem_repeticao_nem': request.form.get('linguagem_repeticao_nem', type=int),
            
            # LINGUAGEM - Nomeação (0-2 pontos)
            'linguagem_nomeacao_caneta': request.form.get('linguagem_nomeacao_caneta', type=int),
            'linguagem_nomeacao_relogio': request.form.get('linguagem_nomeacao_relogio', type=int),
            
            # LINGUAGEM - Compreensão figuras (0-4 pontos)
            'linguagem_monarquia': request.form.get('linguagem_monarquia', type=int),
            'linguagem_pantanal': request.form.get('linguagem_pantanal', type=int),
            'linguagem_antartica': request.form.get('linguagem_antartica', type=int),
            'linguagem_nautica': request.form.get('linguagem_nautica', type=int),
            
            # LINGUAGEM - Leitura (0-1 ponto)
            'linguagem_leitura': request.form.get('linguagem_leitura', type=int),
            
            # HABILIDADES VISUAIS-ESPACIAIS (0-8 pontos)
            'visual_pentagonos': request.form.get('visual_pentagonos', type=int),
            'visual_cubo': request.form.get('visual_cubo', type=int),
            'visual_relogio_circulo': request.form.get('visual_relogio_circulo', type=int),
            'visual_relogio_numeros': request.form.get('visual_relogio_numeros', type=int),
            'visual_relogio_ponteiros': request.form.get('visual_relogio_ponteiros', type=int),
            
            # HABILIDADES PERCEPTIVAS (0-8 pontos)
            'perceptiva_pontos': request.form.get('perceptiva_pontos', type=int),
            'perceptiva_letras': request.form.get('perceptiva_letras', type=int),
            
            # RECORDAÇÃO & RECONHECIMENTO (0-12 pontos)
            'recordacao_renato': request.form.get('recordacao_renato', type=int),
            'recordacao_rua': request.form.get('recordacao_rua', type=int),
            'recordacao_73': request.form.get('recordacao_73', type=int),
            'recordacao_santarem': request.form.get('recordacao_santarem', type=int),
            'recordacao_para': request.form.get('recordacao_para', type=int),
            'reconhecimento_pontos': request.form.get('reconhecimento_pontos', type=int)
        }

        # CALCULA PONTUAÇÃO TOTAL E SUBTOTAIS
        resultados = calcular_pontuacao_acer(dados_acer)
        
        # INTERPRETAÇÃO DO RESULTADO
        pontuacao_total = resultados['total']
        interpretacao = obter_interpretacao_acer(pontuacao_total)
        classificacao = obter_classificacao_acer(pontuacao_total)

        # SALVA NO BANCO DE DADOS
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO aplicacoes_acer 
            (paciente_id, hospital, examinador, escolaridade, profissao, dominancia_manual,
             dados_respostas, pontuacao_total, interpretacao, data_aplicacao,
             subtotal_atencao_orientacao, subtotal_memoria, subtotal_fluencia,
             subtotal_linguagem, subtotal_visual_espacial)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            paciente_id,
            dados_acer['hospital'],
            dados_acer['examinador'],
            dados_acer['escolaridade'],
            dados_acer['profissao'],
            dados_acer['dominancia_manual'],
            str(dados_acer), 
            pontuacao_total, 
            interpretacao,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            resultados['atencao_orientacao'],
            resultados['memoria'],
            resultados['fluencia'],
            resultados['linguagem'],
            resultados['visual_espacial']
        ))
        
        avaliacao_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # SALVA NA SESSÃO
        session['ultima_avaliacao_acer'] = {
            'avaliacao_id': avaliacao_id,
            'pontuacao_total': pontuacao_total,
            'interpretacao': interpretacao,
            'classificacao': classificacao,
            'nome_paciente': paciente_info['nome'],
            'data_aplicacao': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'subtotais': resultados
        }

        # LIMPA sessão
        session.pop('paciente_id', None)

        # REDIRECIONA PARA RESULTADO
        return redirect(url_for('acer.resultado_acer'))

    return render_template('pasta_consulta_medica/pasta_addenbroke_ace/teste_addenbroke_ace.html', 
                         paciente=paciente_info, 
                         data_atual=data_atual)

def calcular_pontuacao_acer(dados):
    """Calcula a pontuação total e subtotais do ACE-R"""
    resultados = {}
    
    # ATENÇÃO & ORIENTAÇÃO (0-18 pontos)
    resultados['atencao_orientacao'] = (
        (dados.get('orientacao_dia_semana', 0) or 0) +
        (dados.get('orientacao_dia_mes', 0) or 0) +
        (dados.get('orientacao_mes', 0) or 0) +
        (dados.get('orientacao_ano', 0) or 0) +
        (dados.get('orientacao_hora', 0) or 0) +
        (dados.get('orientacao_local_especifico', 0) or 0) +
        (dados.get('orientacao_local_generico', 0) or 0) +
        (dados.get('orientacao_bairro', 0) or 0) +
        (dados.get('orientacao_cidade', 0) or 0) +
        (dados.get('orientacao_estado', 0) or 0) +
        (dados.get('subtracao_93', 0) or 0) +
        (dados.get('subtracao_86', 0) or 0) +
        (dados.get('subtracao_79', 0) or 0) +
        (dados.get('subtracao_72', 0) or 0) +
        (dados.get('subtracao_65', 0) or 0)
    )
    
    # MEMÓRIA (0-26 pontos)
    resultados['memoria'] = (
        (dados.get('registro_carro', 0) or 0) +
        (dados.get('registro_vaso', 0) or 0) +
        (dados.get('registro_tijolo', 0) or 0) +
        (dados.get('memoria_carro', 0) or 0) +
        (dados.get('memoria_vaso', 0) or 0) +
        (dados.get('memoria_tijolo', 0) or 0) +
        (dados.get('memoria_renato_t3', 0) or 0) +
        (dados.get('memoria_rua_t3', 0) or 0) +
        (dados.get('memoria_73_t3', 0) or 0) +
        (dados.get('memoria_santarem_t3', 0) or 0) +
        (dados.get('memoria_para_t3', 0) or 0) +
        (dados.get('memoria_presidente_atual', 0) or 0) +
        (dados.get('memoria_presidente_brasilia', 0) or 0) +
        (dados.get('memoria_presidente_eua', 0) or 0) +
        (dados.get('memoria_presidente_eua_assassinado', 0) or 0) +
        (dados.get('recordacao_renato', 0) or 0) +
        (dados.get('recordacao_rua', 0) or 0) +
        (dados.get('recordacao_73', 0) or 0) +
        (dados.get('recordacao_santarem', 0) or 0) +
        (dados.get('recordacao_para', 0) or 0) +
        (dados.get('reconhecimento_pontos', 0) or 0)
    )
    
    # FLUÊNCIA (0-14 pontos)
    resultados['fluencia'] = (
        (dados.get('fluencia_p_pontos', 0) or 0) +
        (dados.get('fluencia_animais_pontos', 0) or 0)
    )
    
    # LINGUAGEM (0-26 pontos)
    resultados['linguagem'] = (
        (dados.get('linguagem_fechar_olhos', 0) or 0) +
        (dados.get('linguagem_pegar_papel', 0) or 0) +
        (dados.get('linguagem_dobrar_papel', 0) or 0) +
        (dados.get('linguagem_colocar_chao', 0) or 0) +
        (dados.get('linguagem_escrita', 0) or 0) +
        (dados.get('linguagem_repeticao_palavras', 0) or 0) +
        (dados.get('linguagem_repeticao_acima', 0) or 0) +
        (dados.get('linguagem_repeticao_nem', 0) or 0) +
        (dados.get('linguagem_nomeacao_caneta', 0) or 0) +
        (dados.get('linguagem_nomeacao_relogio', 0) or 0) +
        (dados.get('linguagem_monarquia', 0) or 0) +
        (dados.get('linguagem_pantanal', 0) or 0) +
        (dados.get('linguagem_antartica', 0) or 0) +
        (dados.get('linguagem_nautica', 0) or 0) +
        (dados.get('linguagem_leitura', 0) or 0)
    )
    
    # VISUAL-ESPACIAL (0-16 pontos)
    resultados['visual_espacial'] = (
        (dados.get('visual_pentagonos', 0) or 0) +
        (dados.get('visual_cubo', 0) or 0) +
        (dados.get('visual_relogio_circulo', 0) or 0) +
        (dados.get('visual_relogio_numeros', 0) or 0) +
        (dados.get('visual_relogio_ponteiros', 0) or 0) +
        (dados.get('perceptiva_pontos', 0) or 0) +
        (dados.get('perceptiva_letras', 0) or 0)
    )
    
    # TOTAL (0-100 pontos)
    resultados['total'] = (
        resultados['atencao_orientacao'] +
        resultados['memoria'] +
        resultados['fluencia'] +
        resultados['linguagem'] +
        resultados['visual_espacial']
    )
    
    return resultados

def obter_interpretacao_acer(pontuacao):
    """Retorna a interpretação baseada na pontuação do ACE-R"""
    if pontuacao >= 88:
        return "Cognição normal"
    elif pontuacao >= 82:
        return "Comprometimento cognitivo muito leve"
    elif pontuacao >= 70:
        return "Comprometimento cognitivo leve"
    elif pontuacao >= 50:
        return "Demência leve a moderada"
    else:
        return "Demência moderada a grave"

def obter_classificacao_acer(pontuacao):
    """Retorna a classificação baseada na pontuação"""
    if pontuacao >= 88:
        return "normal"
    elif pontuacao >= 82:
        return "muito_leve"
    elif pontuacao >= 70:
        return "leve"
    elif pontuacao >= 50:
        return "moderada"
    else:
        return "grave"

@bp_acer.route('/resultado')
def resultado_acer():
    resultado = session.get('ultima_avaliacao_acer', {})
    
    if not resultado:
        flash("Nenhuma avaliação ACE-R encontrada. Por favor, realize uma avaliação primeiro.")
        return redirect(url_for('acer.aplicar_acer'))
    
    return render_template('pasta_consulta_medica/pasta_addenbroke_ace/resultado.html', resultado=resultado)