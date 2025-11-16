from flask import Blueprint, render_template, get_flashed_messages

bp_pagina_inicial = Blueprint('pagina_inicial', __name__)

@bp_pagina_inicial.route('/')
def pagina_inicial():
    return render_template('pagina_inicial.html')
