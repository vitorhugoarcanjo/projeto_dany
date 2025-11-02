from flask import render_template, Blueprint, request, redirect, url_for, session

bp_pagina_7 = Blueprint('pagina_7', __name__)

@bp_pagina_7.route('/', methods=['GET', 'POST'])
def tela_pagina_7():
    if request.method == 'POST':
        dados_pagina_7 = {
            'ansiedade_preocupacao': request.form.get('ansiedade_preocupacao'),
            'ansiedade_relaxar': request.form.get('ansiedade_relaxar'),
            'ansiedade_trivial': request.form.get('ansiedade_trivial'),

            'apatia_interesse': request.form.get('apatia_interesse'),
            'apatia_engajamento': request.form.get('apatia_engajamento'),
            'apatia_indiferente': request.form.get('apatia_indiferente'),

            'desinibicao_impulsivo': request.form.get('desinibicao_impulsivo'),
            'desinibicao_dizer': request.form.get('desinibicao_dizer'),
            'desinibicao_comportamento': request.form.get('desinibicao_comportamento'),
            'desinibicao_personalidade': request.form.get('desinibicao_personalidade'),

            'agitacao_cooperativo': request.form.get('agitacao_cooperativo'),
            'agitacao_ajuda': request.form.get('agitacao_ajuda'),
            'agitacao_agressivo': request.form.get('agitacao_agressivo'),
            'agitacao_ritual': request.form.get('agitacao_ritual')
        }

        atendimento = session.get('atendimento', {})
        atendimento['pagina_7'] = dados_pagina_7
        session['atendimento'] = atendimento

        # Salvar dados e redirecionar
        return redirect(url_for('pagina_8.tela_pagina_8'))
    
    return render_template('pasta_consulta_medica/pagina_7.html')
