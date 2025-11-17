import os
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import re
from config.database import get_db_connection, criar_tabelas

bp_cadastro = Blueprint('cadastro', __name__)

def validar_cpf(cpf):
    return re.match(r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$', cpf) is not None

@bp_cadastro.route('/', methods=['GET', 'POST'])
def cadastro():
    proximo_teste = request.args.get('proximo', 'meem_g.aplicar_meem_g')
    session['proximo_teste'] = proximo_teste
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        data_nascimento = request.form.get('data_nascimento')

        if not validar_cpf(cpf):
            flash('CPF inválido. Use formato 000.000.000-00.', 'error')
            return render_template('pasta_paciente/cadastro_paciente.html', nome=nome, telefone=telefone)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO pacientes (nome, cpf, telefone, data_nascimento) VALUES (?, ?, ?, ?)", 
                         (nome, cpf, telefone, data_nascimento))
            conn.commit()
            paciente_id = cursor.lastrowid
            session['paciente_id'] = paciente_id
            conn.close()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for(proximo_teste))
            
        except sqlite3.IntegrityError:
            conn.close()
            flash('Erro ao cadastrar paciente.', 'error')
            return render_template('pasta_paciente/cadastro_paciente.html', 
                                 nome=nome, cpf=cpf, telefone=telefone, data_nascimento=data_nascimento)

    return render_template('pasta_paciente/cadastro_paciente.html', 
                         nome='', cpf='', telefone='', data_nascimento='')

@bp_cadastro.route('/verificar_cpf', methods=['POST'])
def verificar_cpf():
    cpf = request.json.get('cpf')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone, data_nascimento FROM pacientes WHERE cpf = ?", (cpf,))
    paciente = cursor.fetchone()
    conn.close()

    if paciente:
        session['paciente_id'] = paciente[0]
        proximo_teste = session.get('proximo_teste', 'meem_g.aplicar_meem_g')
        
        return {
            'existe': True,
            'nome': paciente[1],
            'telefone': paciente[2],
            'data_nascimento': paciente[3],
            'redirect_url': url_for(proximo_teste)
        }
    else:
        return {'existe': False}