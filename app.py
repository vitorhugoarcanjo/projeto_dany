from flask import Flask, render_template

# IMPORTAÇÃO DA CHAVE
from utils.config import get_secret_key

# IMPORTAÇÃO DAS PÁGINAS
from config.database import criar_tabelas
from rotas.pasta_paciente.cadastro_paciente import bp_cadastro
# Remove o import do criar_tabela_atendimentos se não for mais usado
from rotas.pagina_inicial import bp_pagina_inicial

# TESTE MEEN_G
from rotas.pasta_consulta_medica.pasta_meen_g.pagina_1_meen_g import bp_meem_g

# TESTE MOCA B
from rotas.pasta_consulta_medica.pasta_moca_b.pagina_2_moca_b import bp_moca_b

# TESTE MOCA
from rotas.pasta_consulta_medica.pasta_moca.pagina_3_moca import bp_moca

# TESTE QUESTIONÁRIO DE ATIVIDADES FUNCIONAIS (Pfeffer)
from rotas.pasta_consulta_medica.pasta_ques_ativ_func.pfeffer import bp_pfeffer


app = Flask(__name__)
app.secret_key = get_secret_key()

# PÁGINA INICIAL
app.register_blueprint(bp_pagina_inicial, url_prefix='/pagina_inicial')

# CADASTRO PACIENTE
app.register_blueprint(bp_cadastro, url_prefix='/cadastro')

# TESTE MEEN_G
app.register_blueprint(bp_meem_g, url_prefix='/meem_g')

# TESTE MOCA B
app.register_blueprint(bp_moca_b, url_prefix='/moca_b')

# TESTE MOCA
app.register_blueprint(bp_moca, url_prefix='/moca')

# TESTE PFEFFER
app.register_blueprint(bp_pfeffer, url_prefix='/pfeffer')


@app.route('/')
def pagina_inicial():
    return render_template('pagina_inicial.html')


if __name__ == '__main__':
    criar_tabelas()  # Só essa função agora
    app.run(debug=True)