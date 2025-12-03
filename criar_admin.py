from werkzeug.security import generate_password_hash
import sqlite3
import os
from pathlib import Path

# Caminho do seu banco
BASE_DIR = Path(__file__).parent
conexao_banco = os.path.join(BASE_DIR, 'instance', 'dany.db')

def criar_admin_automatico():
    """Cria automaticamente o administrador do sistema"""
    
    print("👑 CRIANDO ADMINISTRADOR DO SISTEMA")
    print(f"📁 Banco: {conexao_banco}")
    
    if not os.path.exists(conexao_banco):
        print("❌ Banco de dados não encontrado!")
        print("Execute primeiro: python app.py (para criar o banco)")
        return False
    
    conn = sqlite3.connect(conexao_banco)
    cursor = conn.cursor()
    
    try:
        # 1. Verifica se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='medicos'")
        if not cursor.fetchone():
            print("❌ Tabela 'medicos' não existe!")
            print("Execute primeiro: python app.py para criar as tabelas")
            conn.close()
            return False
        
        print("✅ Tabela 'medicos' encontrada!")
        
        # 2. Verifica se tem a coluna is_admin (se não, adiciona)
        cursor.execute("PRAGMA table_info(medicos)")
        colunas = [col[1] for col in cursor.fetchall()]
        
        if 'is_admin' not in colunas:
            print("➕ Adicionando coluna 'is_admin'...")
            cursor.execute("ALTER TABLE medicos ADD COLUMN is_admin BOOLEAN DEFAULT 0")
            conn.commit()
            print("✅ Coluna 'is_admin' adicionada!")
        
        # 3. Verifica se o admin já existe
        cursor.execute("SELECT id FROM medicos WHERE login = 'admin' AND is_admin = 1")
        if cursor.fetchone():
            print("⚠️ Administrador 'admin' já existe!")
            print("Deseja atualizar a senha?")
            
            # Atualiza a senha do admin existente
            senha_hash = generate_password_hash('admin123')
            cursor.execute("UPDATE medicos SET senha_hash = ? WHERE login = 'admin'", (senha_hash,))
            conn.commit()
            print("✅ Senha do admin atualizada para 'admin123'")
        else:
            # 4. Remove admin antigos se existirem
            cursor.execute("DELETE FROM medicos WHERE login = 'admin'")
            
            # 5. Cria o administrador
            senha_hash = generate_password_hash('admin123')
            
            cursor.execute('''
            INSERT INTO medicos (nome_completo, login, senha_hash, email, cpf, data_nascimento, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                'Administrador do Sistema',
                'admin',  # login
                senha_hash,
                'admin@conectaprev.com',
                '00000000000',
                '1980-01-01',
                1  # is_admin = TRUE
            ))
            
            conn.commit()
            print("✅ Administrador criado com sucesso!")
        
        # 6. Mostra todos os médicos
        cursor.execute("SELECT id, nome_completo, login, email, is_admin FROM medicos ORDER BY is_admin DESC, id")
        medicos = cursor.fetchall()
        
        print("\n" + "="*60)
        print("👑 DADOS DO ADMINISTRADOR")
        print("="*60)
        print("Login: admin")
        print("Senha: admin123")
        print("Email: admin@conectaprev.com")
        print("Nível: Administrador Master")
        print("="*60)
        
        print("\n📋 TODOS OS MÉDICOS NO SISTEMA:")
        print("-"*60)
        
        if medicos:
            for medico in medicos:
                tipo = "👑 ADMIN" if medico[4] else "👨‍⚕️ MÉDICO"
                print(f"{tipo} | ID: {medico[0]:<3} | Login: {medico[2]:<10} | Nome: {medico[1]}")
        else:
            print("Nenhum médico cadastrado (apenas admin foi criado)")
        
        print("-"*60)
        print(f"Total: {len(medicos)} médico(s) cadastrado(s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar administrador: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("SCRIPT DE CONFIGURAÇÃO DO CONECTA PREV")
    print("="*60)
    
    sucesso = criar_admin_automatico()
    
    if sucesso:
        print("\n✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Execute: python app.py")
        print("2. Acesse: http://localhost:5000/")
        print("3. Faça login com:")
        print("   👑 Login: admin")
        print("   🔑 Senha: admin123")
        print("4. No painel, clique em '👑 GERENCIAR MÉDICOS'")
        print("5. Cadastre novos médicos pelo sistema")
        print("\n⚠️  RECOMENDAÇÃO:")
        print("Após usar este script, você pode excluí-lo ou renomeá-lo.")
    else:
        print("\n❌ FALHA NA CONFIGURAÇÃO")
        print("Verifique se o banco de dados foi criado corretamente.")
    
    print("\n" + "="*60)