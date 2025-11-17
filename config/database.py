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
    ''');
    
    conn.commit()
    conn.close()
    print(f"✅ Tabelas verificadas! Banco em: {conexao_banco}")