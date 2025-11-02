from flask import render_template, Blueprint, request, redirect, url_for, session

bp_pagina_8 = Blueprint('pagina_8', __name__)

@bp_pagina_8.route('/', methods=['GET', 'POST'])
def tela_pagina_8():
    if request.method == 'POST':

        dados_pagina_8 = {
            'delirios': request.form.get('delirios'),
            'ouvir_vozes': request.form.get('ouvir_vozes'),
            'conversa_sozinho': request.form.get('conversa_sozinho'),
            'ver_coisas': request.form.get('ver_coisas'),

            'mudanca_apetite': request.form.get('mudanca_apetite'),
            'mudanca_preferencia': request.form.get('mudanca_preferencia'),

            'dificuldades_sono': request.form.get('dificuldades_sono'),
            'movimentos_sono': request.form.get('movimentos_sono'),
            'roncos': request.form.get('roncos'),
            'sonolencia_diurna': request.form.get('sonolencia_diurna')
        }

        # Salvar dados sessao
        atendimento = session.get('atendimento', {})
        atendimento['pagina_8'] = dados_pagina_8
        session['atendimento'] = atendimento


        return redirect(url_for('final.tela_final'))  # ajustar conforme sua rota final
    
    return render_template('pasta_consulta_medica/pagina_8.html')
