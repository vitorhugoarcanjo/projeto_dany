from flask import render_template, request, redirect, Blueprint, url_for, session

bp_pagina_3 = Blueprint('pagina_3', __name__)

@bp_pagina_3.route('/', methods=['GET', 'POST'])
def tela_pagina_3():
    if request.method == 'POST':

        # GUARDAR DADOS PAGINA 3
        dados_pagina_3 = {
            'perda_olfato': request.form.get('perda_olfato'),
            'esquecimentos': request.form.get('esquecimentos'),
            'mudanca_humor': request.form.get('mudanca_humor'),
            'qual_humor': request.form.get('qual_humor'),
            'rigidez': request.form.get('rigidez'),
            'diminuicao_tonus': request.form.get('diminuicao_tonus'),
            'movimentos_faciais': request.form.get('movimentos_faciais')
        }

        # CRIANDO SESSÃO
        atendimento = session.get('atendimento', {})
        atendimento['pagina_3'] = dados_pagina_3
        session['atendimento'] = atendimento

        # VOU PENSAR - SALVAR BANCO DE DADOS E SESSÃO

        return redirect(url_for('pagina_4.tela_pagina_4'))
    
    return render_template('pasta_consulta_medica/pagina_3.html')