import os
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import re
from config.database import get_db_connection, criar_tabelas

bp_cadastro = Blueprint('cadastro', __name__)

def validar_cpf(cpf):
    return re.match(r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$', cpf) is not None

@bp_cadastro.route('/', methods=['GET', 'POST'])
def cadastro():
    # ✅ PRIMEIRO pega da URL ou da sessão
    proximo_teste = request.args.get('proximo')

    # ✅ SALVA na sessão SEMPRE que vier da URL
    if proximo_teste:
        session['proximo_teste'] = proximo_teste
    else:
        proximo_teste = session.get('proximo_teste')
    
    print(f"🔍 DEBUG - Próximo teste: {proximo_teste}")
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        data_nascimento = request.form.get('data_nascimento')

        if not validar_cpf(cpf):
            flash('CPF inválido. Use formato 000.000.000-00.', 'error')
            return render_template('pasta_paciente/cadastro_paciente.html', 
                                 nome=nome, telefone=telefone, 
                                 proximo_teste=proximo_teste)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO pacientes (nome, cpf, telefone, data_nascimento) VALUES (?, ?, ?, ?)", 
                         (nome, cpf, telefone, data_nascimento))
            conn.commit()
            paciente_id = cursor.lastrowid
            session['paciente_id'] = paciente_id
            conn.close()
            
            print(f"🔍 DEBUG - Redirecionando para: {proximo_teste}")
            
            if proximo_teste:
                flash('Cadastro realizado com sucesso!', 'success')
                return redirect(url_for(proximo_teste))
            else:
                flash('Cadastro realizado com sucesso!', 'success')
                return redirect(url_for('cadastro.cadastro'))
            
        except sqlite3.IntegrityError:
            conn.close()
            flash('Erro: CPF já cadastrado no sistema.', 'error')
            return render_template('pasta_paciente/cadastro_paciente.html', 
                                 nome=nome, cpf=cpf, telefone=telefone, 
                                 data_nascimento=data_nascimento,
                                 proximo_teste=proximo_teste)

    return render_template('pasta_paciente/cadastro_paciente.html', 
                         nome='', cpf='', telefone='', data_nascimento='',
                         proximo_teste=proximo_teste)  # ✅ IMPORTANTE: passar para o template

@bp_cadastro.route('/verificar_cpf', methods=['POST'])
def verificar_cpf():
    cpf = request.json.get('cpf')
    
    if not cpf:
        return jsonify({'existe': False, 'error': 'CPF não fornecido'})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone, data_nascimento FROM pacientes WHERE cpf = ?", (cpf,))
    paciente = cursor.fetchone()
    conn.close()

    if paciente:
        session['paciente_id'] = paciente[0]
        proximo_teste = session.get('proximo_teste')
        
        print(f"🔍 DEBUG - Próximo teste na verificação: {proximo_teste}")
        
        response_data = {
            'existe': True,
            'nome': paciente[1],
            'telefone': paciente[2],
            'data_nascimento': paciente[3],
            'paciente_id': paciente[0],
            'proximo_teste': proximo_teste  # ✅ Envia também para o frontend
        }
        
        # ✅ SÓ envia redirect_url se proximo_teste existir
        if proximo_teste:
            try:
                response_data['redirect_url'] = url_for(proximo_teste)
                print(f"✅ URL gerada: {response_data['redirect_url']}")
            except Exception as e:
                response_data['error'] = f'Erro ao gerar URL: {str(e)}'
                print(f"❌ Erro ao gerar URL: {e}")
        else:
            response_data['warning'] = 'Nenhum teste selecionado.'
        
        return jsonify(response_data)
    else:
        return jsonify({'existe': False})

@bp_cadastro.route('/limpar_sessao')
def limpar_sessao():
    session.pop('paciente_id', None)
    session.pop('proximo_teste', None)
    flash('Sessão limpa. Você pode iniciar um novo cadastro.', 'info')
    return redirect(url_for('cadastro.cadastro'))