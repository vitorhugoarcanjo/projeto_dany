from flask import render_template, redirect, url_for, Blueprint, request, session

bp_pagina_5 = Blueprint('pagina_5', __name__)

@bp_pagina_5.route('/', methods=['GET', 'POST'])
def tela_pagina_5():
    if request.method == 'POST':
        # GUARDAR DADOS PAGINA_5
        dados_pagina_5 = {
            'momentos_confusos': request.form.get('momentos_confusos'),
            'facilidade_distraicao': request.form.get('facilidade_distraicao'),
            'esquecimento_objetos': request.form.get('esquecimento_objetos'),
            'dificuldade_memoria': request.form.get('dificuldade_memoria'),
            'desorientacao_temporal': request.form.get('desorientacao_temporal'),
            'conversas_repetitivas': request.form.get('conversas_repetitivas'),
            'anotacoes_necessarias': request.form.get('anotacoes_necessarias'),
            'esquecimentos_compromissos': request.form.get('esquecimentos_compromissos'),

            'dificuldade_palavras': request.form.get('dificuldade_palavras'),
            'nomear_objetos': request.form.get('nomear_objetos'),
            'articular_palavras': request.form.get('articular_palavras'),
            'compreender_falado': request.form.get('compreender_falado'),

            'perdido_caminhos': request.form.get('perdido_caminhos'),
            'aprender_caminhos': request.form.get('aprender_caminhos'),
            'dificuldade_localizar': request.form.get('dificuldade_localizar'),

            'dificuldade_praxias': request.form.get('dificuldade_praxias'),
            'dificuldade_vestir': request.form.get('dificuldade_vestir'),

            'dificuldade_planejar': request.form.get('dificuldade_planejar'),
            'dificuldade_etapas': request.form.get('dificuldade_etapas'),
            'dificuldade_resolver': request.form.get('dificuldade_resolver'),
            'dificuldade_decisoes': request.form.get('dificuldade_decisoes')  
        }

        # Salvar dados
        atendimento = session.get('atendimento', {})
        atendimento['pagina_5'] = dados_pagina_5
        session['atendimento'] = atendimento

        return redirect(url_for('pagina_6.tela_pagina_6'))  # Ajuste conforme próximo bloco
    
    return render_template('pasta_consulta_medica/pagina_5.html')