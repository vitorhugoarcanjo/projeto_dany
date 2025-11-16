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


from rotas.pasta_consulta_medica.pagina_3 import bp_pagina_3
from rotas.pasta_consulta_medica.pagina_4 import bp_pagina_4
from rotas.pasta_consulta_medica.pagina_5 import bp_pagina_5
from rotas.pasta_consulta_medica.pagina_6 import bp_pagina_6
from rotas.pasta_consulta_medica.pagina_7 import bp_pagina_7
from rotas.pasta_consulta_medica.pagina_8 import bp_pagina_8
from rotas.pasta_consulta_medica.pagina_final import bp_final

app = Flask(__name__)
app.secret_key = get_secret_key()

# PÁGINA INICIAL
app.register_blueprint(bp_pagina_inicial, url_prefix='/pagina_inicial')

# CADASTRO PACIENTE
app.register_blueprint(bp_cadastro, url_prefix='/cadastro')

# TESTE MEEN_G
app.register_blueprint(bp_meem_g, url_prefix='/meen_g')

# TESTE MOCA B
app.register_blueprint(bp_moca_b, url_prefix='/moca_b')


# PÁGINA 3
app.register_blueprint(bp_pagina_3, url_prefix='/pagina_3')

# PÁGINA 4
app.register_blueprint(bp_pagina_4, url_prefix='/pagina_4')

# PÁGINA 5
app.register_blueprint(bp_pagina_5, url_prefix='/pagina_5')

# PÁGINA 6
app.register_blueprint(bp_pagina_6, url_prefix='/pagina_6')

# PÁGINA 7
app.register_blueprint(bp_pagina_7, url_prefix='/pagina_7')

# PÁGINA 8
app.register_blueprint(bp_pagina_8, url_prefix='/pagina_8')

# PÁGINA FINAL
app.register_blueprint(bp_final, url_prefix='/final')


@app.route('/')
def pagina_inicial():
    return render_template('pagina_inicial.html')


if __name__ == '__main__':
    criar_tabelas()  # Só essa função agora
    app.run(debug=True)