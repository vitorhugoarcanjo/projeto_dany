from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from config.database import get_db_connection  # IMPORTA A CONEXÃO DO SEU BANCO

bp_login = Blueprint('login', __name__)

@bp_login.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('medico_logado'):
        return redirect(url_for('pos_login'))
    
    if request.method == 'POST':
        login_usuario = request.form['login']
        senha = request.form['senha']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM medicos WHERE login = ?', (login_usuario,))
        medico = cursor.fetchone()
        conn.close()
        
        if medico and check_password_hash(medico[3], senha):  # índice 3 = senha_hash
            session['medico_logado'] = True
            session['medico_id'] = medico[0]
            session['medico_nome'] = medico[1]
            session['is_admin'] = bool(medico[7]) if len(medico) > 7 else False  # índice 7 = is_admin
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('pos_login'))
        else:
            flash('Login ou senha incorretos!', 'error')
    
    return render_template('pasta_login/login.html')

@bp_login.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('pagina_inicial'))


@bp_login.route('/cadastro_medico', methods=['GET', 'POST'])
def cadastro_medico():
    if request.method == 'POST':
        # Coletar dados do formulário
        nome_completo = request.form.get('nome_completo', '').strip()
        login = request.form.get('login', '').strip()
        senha = request.form.get('senha', '')
        confirmar_senha = request.form.get('confirmar_senha', '')
        email = request.form.get('email', '').strip()
        cpf = request.form.get('cpf', '').replace('.', '').replace('-', '').strip()
        data_nascimento = request.form.get('data_nascimento', '')
        
        # Validações
        erros = []
        
        if not all([nome_completo, login, senha, email, cpf, data_nascimento]):
            erros.append('Todos os campos são obrigatórios!')
        
        if senha != confirmar_senha:
            erros.append('As senhas não coincidem!')
        
        if len(senha) < 6:
            erros.append('A senha deve ter pelo menos 6 caracteres!')
        
        # Validar CPF (11 dígitos)
        if len(cpf) != 11 or not cpf.isdigit():
            erros.append('CPF inválido! Deve conter 11 dígitos.')
        
        # Validar data (mínimo 18 anos)
        from datetime import datetime, date
        try:
            data_nasc = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            hoje = date.today()
            idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
            if idade < 18:
                erros.append('O médico deve ter pelo menos 18 anos!')
        except ValueError:
            erros.append('Data de nascimento inválida!')
        
        if erros:
            for erro in erros:
                flash(erro, 'error')
            return render_template('pasta_cadastro_medico/cadastro_medico.html')
        
        # Se passou nas validações, salva no banco
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar se login, email ou CPF já existem
            cursor.execute('SELECT login FROM medicos WHERE login = ?', (login,))
            if cursor.fetchone():
                flash('Login já existe! Escolha outro.', 'error')
                return render_template('pasta_cadastro_medico/cadastro_medico.html')
            
            cursor.execute('SELECT email FROM medicos WHERE email = ?', (email,))
            if cursor.fetchone():
                flash('E-mail já cadastrado!', 'error')
                return render_template('pasta_cadastro_medico/cadastro_medico.html')
            
            cursor.execute('SELECT cpf FROM medicos WHERE cpf = ?', (cpf,))
            if cursor.fetchone():
                flash('CPF já cadastrado!', 'error')
                return render_template('pasta_cadastro_medico/cadastro_medico.html')
            
            # Inserir novo médico
            cursor.execute('''
            INSERT INTO medicos (nome_completo, login, senha_hash, email, cpf, data_nascimento)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                nome_completo,
                login,
                generate_password_hash(senha),
                email,
                cpf,
                data_nascimento
            ))
            
            conn.commit()
            conn.close()
            
            flash(f'Médico {nome_completo} cadastrado com sucesso!', 'success')
            return redirect(url_for('pos_login'))
            
        except Exception as e:
            flash(f'Erro no cadastro: {str(e)}', 'error')
    
    # GET request - mostrar formulário
    # Calcular data máxima (18 anos atrás)
    from datetime import date, timedelta
    data_maxima = date.today() - timedelta(days=365*18)
    
    return render_template('pasta_cadastro_medico/tela_cadastro_medico.html', 
                          data_maxima=data_maxima.strftime('%Y-%m-%d'))




@bp_login.route('/gerenciar_medicos')
def gerenciar_medicos():
    # Verifica se é administrador
    if not session.get('is_admin'):
        flash('Acesso restrito apenas para administradores!', 'error')
        return redirect(url_for('pos_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, nome_completo, login, email, cpf, 
           strftime('%d/%m/%Y', data_nascimento) as data_nasc,
           is_admin,
           strftime('%d/%m/%Y %H:%M', data_cadastro) as cadastro
    FROM medicos 
    ORDER BY is_admin DESC, nome_completo
    ''')
    medicos = cursor.fetchall()
    conn.close()
    
    return render_template('pasta_cadastro_medico/gerenciar_medicos.html', medicos=medicos)