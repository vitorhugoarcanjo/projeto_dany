from flask import render_template, Blueprint, redirect, request, url_for, session

bp_pagina_2 = Blueprint('pagina_2', __name__)


@bp_pagina_2.route('/', methods=['GET', 'POST'])
def tela_pagina_2():
    if request.method == 'POST':

        # GUARDAR DADOS PAGINA 2
        dados_pagina_2 = {
            'fuma': request.form.get('fuma'),
            'bebe': request.form.get('bebe'),
            'drogas': request.form.get('drogas'),
            'remedios': request.form.get('remedios'),
            'horas_sono': request.form.get('horas_sono'),
            'insonia': request.form.get('insonia'),
            'atividade': request.form.get('atividade'),
            'frequencia': request.form.get('frequencia')
        }

        atendimento = session.get('atendimento', {})
        atendimento['pagina_2'] = dados_pagina_2
        session['atendimento'] = atendimento

        # VOU PENSAR - SALVAR BANCO E SESSÃO

        return redirect(url_for('pagina_3.tela_pagina_3'))
    
    return render_template('pasta_consulta_medica/pagina_2.html')