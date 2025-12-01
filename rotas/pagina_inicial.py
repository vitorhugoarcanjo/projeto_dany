from flask import Blueprint, render_template, get_flashed_messages, session, url_for, redirect

bp_pagina_inicial = Blueprint('pagina_inicial', __name__)

@bp_pagina_inicial.route('/')
def pagina_inicial():
    return render_template('pagina_inicial.html')

# ADICIONA ESSA ROTA NOVA
@bp_pagina_inicial.route('/escolher_teste/<string:nome_teste>')
def escolher_teste(nome_teste):
    # ✅ LIMPA sessão anterior para evitar conflitos
    session.clear()
    
    # ✅ SALVA o teste escolhido
    session['proximo_teste'] = nome_teste

    
    # ✅ Redireciona pro cadastro COM parâmetro na URL
    return redirect(url_for('cadastro.cadastro', proximo=nome_teste))