import os
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
import re


bp_cadastro = Blueprint('cadastro', __name__)

# Caminho absoluto pro banco dentro da pasta instance
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
conexao_banco = os.path.join(BASE_DIR, '../../instance/dany.db')


def criar_tabela():
    conn = sqlite3.connect(conexao_banco)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        telefone TEXT
    )
    ''')
    conn.commit()
    conn.close()



def validar_cpf(cpf):
    # Validação simples só formato (000.000.000-00)
    return re.match(r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$', cpf) is not None



@bp_cadastro.route('/', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        data_nascimento = request.form.get('data_nascimento')

        if not validar_cpf(cpf):
            flash('CPF inválido. Use formato 000.000.000-00.', 'error')
            return render_template('pasta_paciente/cadastro_paciente.html', nome=nome, telefone=telefone)




        conn = sqlite3.connect(conexao_banco)
        cursor = conn.cursor()

        # SE NÃO EXISTIR, vai criar um novo
        try:
            cursor.execute("INSERT INTO pacientes (nome, cpf, telefone, data_nascimento) VALUES (?, ?, ?, ?)", (nome, cpf, telefone, data_nascimento))
            conn.commit()
            paciente_id = cursor.lastrowid
            session['paciente_id'] = paciente_id
            conn.close()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('pagina_1.tela_pagina_1'))
        except sqlite3.IntegrityError:
            conn.close()
            flash('Erro ao cadastrar paciente.', 'error')
            return render_template('pasta_paciente/cadastro_paciente.html', nome=nome, cpf=cpf, telefone=telefone, data_nascimento=data_nascimento)

    return render_template('pasta_paciente/cadastro_paciente.html', nome='', cpf='', telefone='', data_nascimento='')




@bp_cadastro.route('/verificar_cpf', methods=['POST'])
def verificar_cpf():
    cpf = request.json.get('cpf')
    conn = sqlite3.connect(conexao_banco)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone, data_nascimento FROM pacientes WHERE cpf = ?", (cpf,))
    paciente = cursor.fetchone()
    conn.close()

    if paciente:
        session['paciente_id'] = paciente[0]  # Guarda o id na sessão
        return {
            'existe': True,
            'nome': paciente[1],
            'telefone': paciente[2],
            'data_nascimento': paciente[3]
        }
    else:
        return {'existe': False}



