from werkzeug.security import generate_password_hash
import sqlite3
import os
from pathlib import Path

# Caminho do seu banco (mesmo do seu database.py)
BASE_DIR = Path(__file__).parent
conexao_banco = os.path.join(BASE_DIR, 'instance', 'dany.db')

def criar_medico_manual():
    """Cria um médico com login 1 e senha 13579"""
    
    print("🔍 Conectando ao banco...")
    print(f"📁 Caminho: {conexao_banco}")
    
    # Verifica se o banco existe
    if not os.path.exists(conexao_banco):
        print("❌ Banco de dados não encontrado!")
        print("Execute primeiro: python app.py (para criar as tabelas)")
        return
    
    conn = sqlite3.connect(conexao_banco)
    cursor = conn.cursor()
    
    try:
        # 1. Verifica se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='medicos'")
        if not cursor.fetchone():
            print("❌ Tabela 'medicos' não existe!")
            print("Execute primeiro: python app.py (para criar as tabelas)")
            conn.close()
            return
        
        print("✅ Tabela 'medicos' encontrada!")
        
        # 2. Verifica se o médico já existe
        cursor.execute("SELECT id FROM medicos WHERE login = '1'")
        if cursor.fetchone():
            print("⚠️ Médico com login '1' já existe!")
            opcao = input("Deseja atualizar a senha? (s/n): ").lower()
            if opcao == 's':
                # Atualiza a senha
                senha_hash = generate_password_hash('13579')
                cursor.execute("UPDATE medicos SET senha_hash = ? WHERE login = '1'", (senha_hash,))
                conn.commit()
                print("✅ Senha atualizada para '13579'!")
            else:
                print("Operação cancelada.")
            conn.close()
            return
        
        # 3. Cria o hash da senha '13579'
        senha_hash = generate_password_hash('13579')
        
        # 4. Insere o médico
        cursor.execute('''
        INSERT INTO medicos (nome_completo, login, senha_hash, email, cpf, data_nascimento)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            'Dr. Médico Teste',
            '1',  # login
            senha_hash,
            'medico1@teste.com',
            '11122233344',
            '1985-05-15'
        ))
        
        conn.commit()
        
        print("\n" + "="*50)
        print("✅ MÉDICO CRIADO COM SUCESSO!")
        print("="*50)
        print("Login: 1")
        print("Senha: 13579")
        print("Nome: Dr. Médico Teste")
        print("Email: medico1@teste.com")
        print("CPF: 111.222.333-44")
        print("Data Nasc.: 15/05/1985")
        print("="*50)
        
        # 5. Mostra todos os médicos
        cursor.execute("SELECT id, nome_completo, login, email FROM medicos ORDER BY id")
        medicos = cursor.fetchall()
        
        print("\n📋 TODOS OS MÉDICOS CADASTRADOS:")
        print("-"*50)
        for medico in medicos:
            print(f"ID: {medico[0]} | Login: {medico[2]} | Nome: {medico[1]} | Email: {medico[3]}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    criar_medico_manual()
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Execute: python app.py")
    print("2. Acesse: http://localhost:5000/")
    print("3. Clique em 'ACESSAR SISTEMA'")
    print("4. Use login: 1 e senha: 13579")