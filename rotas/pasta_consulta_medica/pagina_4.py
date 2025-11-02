from flask import render_template, redirect, url_for, request, Blueprint, session

bp_pagina_4 = Blueprint('pagina_4', __name__)


@bp_pagina_4.route('/', methods=['GET', 'POST'])
def tela_pagina_4():
    if request.method == 'POST':
        
        # GUARDAR DADOS PAGINA 4
        dados_pagina_4 = {
            'pestanejar': request.form.get('pestanejar'),
            'deglutir': request.form.get('deglutir'),
            'cialorreia': request.form.get('cialorreia'),
            'lentidao_pronuncia': request.form.get('lentidao_pronuncia'),
            'gagueira': request.form.get('gagueira'),
            'diminuicao_tom': request.form.get('diminuicao_tom'),
            'dificuldade_mandibular': request.form.get('dificuldade_mandibular')
        }

        # GUARDAR SESSAO
        atendimento = session.get('atendimento', {})
        atendimento['pagina_4'] = dados_pagina_4
        session['atendimento'] = atendimento

        return redirect(url_for('pagina_5.tela_pagina_5'))
    
        # VOU PENSAR - SALVAR BANCO DE DADOS E SESSÃO

    return render_template('pasta_consulta_medica/pagina_4.html')