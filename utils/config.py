import os

def get_secret_key():
    # Pode usar variável de ambiente ou gerar fixa aqui
    return os.environ.get('FLASK_SECRET_KEY', 'uma_chave_super_secreta_e_forte')
