from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3, os


bp_pagina_1 = Blueprint('pagina_1', __name__)


@bp_pagina_1.route('/', methods=['GET', 'POST'])
def tela_pagina_1():
    # Verifica se paciente está logado no início
    if 'paciente_id' not in session:
        return redirect(url_for('cadastro.cadastro'))

    if request.method == 'POST':

        dados_pagina_1 = {
            'dia': request.form.get('dia'),
            'doenca': request.form.get('doenca'),
            'doenca_qual': request.form.get('doenca_qual'),
            'tratamento': request.form.get('tratamento'),
            'tratamento_qual': request.form.get('tratamento_qual'),
            'pessoas': request.form.get('pessoas'),
            'relacao': request.form.get('relacao'),
        }

        # PEGA O DICIONÁRIO EXISTENTE OU CRIA NOVO
        atendimento = session.get('atendimento', {})

        # ATUALIZA O DICIONÁRIO COM OS DADOS DA PÁGINA ATUAL
        atendimento['pagina_1'] = dados_pagina_1

        # SALVA O DICIONARIO ATUALIZADO NA SESSÃO
        session['atendimento'] = atendimento

        return redirect(url_for('pagina_2.tela_pagina_2'))

    return render_template('pasta_consulta_medica/pagina_1.html')
