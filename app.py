from flask import Flask, render_template

# IMPORTAÇÃO DA CHAVE
from utils.config import get_secret_key

# IMPORTAÇÃO DAS PÁGINAS
from rotas.pasta_paciente.cadastro_paciente import bp_cadastro, criar_tabela
from rotas.pasta_paciente.tabela_consultas_salvas.tabela_salvar_consulta import criar_tabela_atendimentos
from rotas.pagina_inicial import bp_pagina_inicial
from rotas.pasta_consulta_medica.pagina_1 import bp_pagina_1
from rotas.pasta_consulta_medica.pagina_2 import bp_pagina_2
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

# PÁGINA 1
app.register_blueprint(bp_pagina_1, url_prefix='/pagina_1')

# PÁGINA 2
app.register_blueprint(bp_pagina_2, url_prefix='/pagina_2')

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
    criar_tabela()
    criar_tabela_atendimentos()
    app.run(debug=True)