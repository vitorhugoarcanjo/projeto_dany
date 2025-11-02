from flask import render_template, Blueprint, request, redirect, url_for, session

bp_pagina_6 = Blueprint('pagina_6', __name__)

@bp_pagina_6.route('/', methods=['GET', 'POST'])
def tela_pagina_6():
    if request.method == 'POST':
        # GUARDAR DADOS
        dados_pagina_6 = {
            'dificuldades_aivds': request.form.get('dificuldades_aivds'),
            'compras': request.form.get('compras'),
            'rendimento_trabalho': request.form.get('rendimento_trabalho'),
            'preparacao_refeicoes': request.form.get('preparacao_refeicoes'),

            'atividades_basicas': request.form.getlist('atividades_basicas'),

            'humor_tristeza': request.form.get('humor_tristeza'),
            'humor_ira': request.form.get('humor_ira'),
            'humor_isolamento': request.form.get('humor_isolamento')

        }

        # SALVAR SESSÃO
        atendimento = session.get('atendimento', {})
        atendimento['pagina_6'] = dados_pagina_6
        session['atendimento'] = atendimento

        return redirect(url_for('pagina_7.tela_pagina_7'))  # ajustar para próxima página
    
    return render_template('pasta_consulta_medica/pagina_6.html')
