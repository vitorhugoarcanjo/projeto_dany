import os
import sqlite3
from pathlib import Path

# CAMINHO UNIVERSAL - instance/dany.db
BASE_DIR = Path(__file__).parent.parent
conexao_banco = os.path.join(BASE_DIR, 'instance', 'dany.db')

def get_db_connection():
    """Retorna conexão com o banco"""
    return sqlite3.connect(conexao_banco)

def criar_tabelas():
    """Cria todas as tabelas necessárias"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela pacientes (SE JÁ EXISTIR, NÃO CRIA DE NOVO)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        telefone TEXT,
        data_nascimento DATE
    )
    ''')
    
    # Tabela do MEEM-G
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aplicacoes_meem_g (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        dados_respostas TEXT NOT NULL,
        pontuacao_total INTEGER NOT NULL,
        interpretacao TEXT NOT NULL,
        data_aplicacao DATETIME NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
    )
    ''')


    # Tabela do MOCA_B
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aplicacoes_moca_b (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        dados_respostas TEXT NOT NULL,
        pontuacao_total INTEGER NOT NULL,
        interpretacao TEXT NOT NULL,
        data_aplicacao DATETIME NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
    )
    ''')


    # TABELA MOCA
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aplicacoes_moca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        escolaridade TEXT,
        dados_respostas TEXT,
        pontuacao_total INTEGER,
        interpretacao TEXT,
        data_aplicacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
    )
    ''')

    # QUESTIONÁRIO DE ATIVIDADES FUNCIONAIS (Pfeffer) 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aplicacoes_pfeffer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        informante TEXT,
        parentesco TEXT,
        dados_respostas TEXT,
        pontuacao_total INTEGER,
        interpretacao TEXT,
        data_aplicacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
    )
    ''')


    # DESENHO RELOGIO
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aplicacoes_relogio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        dados_respostas TEXT,
        pontuacao_total INTEGER,
        interpretacao TEXT,
        data_aplicacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
    )
    ''')

    
    # TESTE ADDENBROKE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aplicacoes_acer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        hospital TEXT,
        examinador TEXT,
        escolaridade TEXT,
        profissao TEXT,
        dominancia_manual TEXT,
        dados_respostas TEXT,
        pontuacao_total INTEGER,
        interpretacao TEXT,
        data_aplicacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        subtotal_atencao_orientacao INTEGER,
        subtotal_memoria INTEGER,
        subtotal_fluencia INTEGER,
        subtotal_linguagem INTEGER,
        subtotal_visual_espacial INTEGER,
        FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
    )
    ''')

        # NOVA TABELA: médicos
    # No seu config/database.py, adicione a coluna is_admin
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        cpf TEXT UNIQUE NOT NULL,
        data_nascimento DATE NOT NULL,
        is_admin BOOLEAN DEFAULT 0,  -- NOVA COLUNA: 0 = médico comum, 1 = administrador
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()
    print(f"✅ Tabelas verificadas! Banco em: {conexao_banco}")