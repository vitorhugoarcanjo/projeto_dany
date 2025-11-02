import sqlite3
import os

# Caminho absoluto pro banco dentro da pasta instance
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
conexao_banco = os.path.join(BASE_DIR, '../../../instance/dany.db')

def criar_tabela_atendimentos():
    dir_banco = os.path.dirname(conexao_banco)
    if not os.path.exists(dir_banco):
        os.makedirs(dir_banco)

    conn = sqlite3.connect(conexao_banco)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            dados TEXT NOT NULL,
            data_atendimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        )
    ''')
    conn.commit()
    conn.close()
