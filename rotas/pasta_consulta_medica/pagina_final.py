import json
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import os

# Caminho absoluto pro banco dentro da pasta instance
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
conexao_banco = os.path.join(BASE_DIR, '../../instance/dany.db')

bp_final = Blueprint('final', __name__)

@bp_final.route('/', methods=['GET', 'POST'])
def tela_final():

    titulos_paginas = {
        'pagina_1': 'Informações Iniciais',
        'pagina_2': 'Hábitos de Vida',
        'pagina_3': 'Sintomas Cognitivos',
        'pagina_4': 'Sintomas Motores',
        'pagina_5': 'Memória e Orientação',
        'pagina_6': 'Atividades Diárias',
        'pagina_7': 'Aspectos Emocionais',
        'pagina_8': 'Sintomas Adicionais'
    }

    nomes_campos = {
        'pagina_1': {
            'dia': 'Como foi o dia',
            'doenca': 'Doença',
            'doenca_qual': 'Qual Doença',
            'tratamento': 'Tratamento',
            'tratamento_qual': 'Qual Tratamento',
            'pessoas': 'Mora quantas pessoas em sua residência',
            'relacao': 'Com quem você se relaciona melhor',
        },
        'pagina_2': {
            'fuma': 'Fuma',
            'bebe': 'Bebe Álcool',
            'drogas': 'Uso de Drogas',
            'remedios': 'Uso de Remédios',
            'horas_sono': 'Horas de Sono',
            'insonia': 'Insônia',
            'atividade': 'Atividade Física',
            'frequencia': 'Qual',
        },
        'pagina_3': {
            'perda_olfato': 'Perda de Olfato',
            'esquecimentos': 'Esquecimentos Frequentes',
            'mudanca_humor': 'Mudança de Humor',
            'qual_humor': 'Qual Humor',
            'rigidez': 'Rigidez',
            'diminuicao_tonus': 'Diminuição do Tônus',
            'movimentos_faciais': 'Movimentos Faciais',
        },
        'pagina_4': {
            'pestanejar': 'Dificuldade em Pestanejar',
            'deglutir': 'Dificuldade para Deglutir',
            'cialorreia': 'Cialorreia',
            'lentidao_pronuncia': 'Lentidão na Pronúncia',
            'gagueira': 'Gagueira',
            'diminuicao_tom': 'Diminuição do Tom',
            'dificuldade_mandibular': 'Dificuldade Mandibular',
        },
        'pagina_5': {
            'momentos_confusos': 'Momentos Confusos',
            'facilidade_distraicao': 'Facilidade para se Distrair',
            'esquecimento_objetos': 'Esquecimento de Objetos',
            'dificuldade_memoria': 'Dificuldade de Memória',
            'desorientacao_temporal': 'Desorientação Temporal',
            'conversas_repetitivas': 'Conversas Repetitivas',
            'anotacoes_necessarias': 'Anotações Necessárias',
            'esquecimentos_compromissos': 'Esquecimento de Compromissos',
            'dificuldade_palavras': 'Dificuldade com Palavras',
            'nomear_objetos': 'Dificuldade em Nomear Objetos',
            'articular_palavras': 'Dificuldade em Articular Palavras',
            'compreender_falado': 'Dificuldade em Compreender o Falado',
            'perdido_caminhos': 'Perda de Caminhos',
            'aprender_caminhos': 'Dificuldade em Aprender Caminhos',
            'dificuldade_localizar': 'Dificuldade em Localizar',
            'dificuldade_praxias': 'Dificuldade em Praxias',
            'dificuldade_vestir': 'Dificuldade em Vestir-se',
            'dificuldade_planejar': 'Dificuldade em Planejar',
            'dificuldade_etapas': 'Dificuldade em Seguir Etapas',
            'dificuldade_resolver': 'Dificuldade em Resolver Problemas',
            'dificuldade_decisoes': 'Dificuldade em Tomar Decisões',
        },
        'pagina_6': {
            'dificuldades_aivds': '[translate:Dificuldades nas Atividades Instrumentais da Vida Diária]',
            'compras': 'Dificuldade para Compras',
            'rendimento_trabalho': 'Rendimento no Trabalho',
            'preparacao_refeicoes': 'Preparação de Refeições',
            'atividades_basicas': 'Atividades Básicas',
            'humor_tristeza': 'Humor - Tristeza',
            'humor_ira': 'Humor - Ira',
            'humor_isolamento': 'Humor - Isolamento',
        },
        'pagina_7': {
            'ansiedade_preocupacao': 'Ansiedade - Preocupação',
            'ansiedade_relaxar': 'Ansiedade - Relaxar',
            'ansiedade_trivial': 'Ansiedade - Situações Triviais',
            'apatia_interesse': 'Apátia - Interesse',
            'apatia_engajamento': 'Apátia - Engajamento',
            'apatia_indiferente': 'Apátia - Indiferença',
            'desinibicao_impulsivo': 'Desinibição - Impulsivo',
            'desinibicao_dizer': 'Desinibição - Dizer',
            'desinibicao_comportamento': 'Desinibição - Comportamento',
            'desinibicao_personalidade': 'Desinibição - Personalidade',
            'agitacao_cooperativo': 'Agitação - Cooperativo',
            'agitacao_ajuda': 'Agitação - Pede Ajuda',
            'agitacao_agressivo': 'Agitação - Agressivo',
            'agitacao_ritual': 'Agitação - Ritual',
        },
        'pagina_8': {
            'delirios': 'Delírios',
            'ouvir_vozes': 'Ouvir Vozes',
            'conversa_sozinho': 'Conversa Sozinho',
            'ver_coisas': 'Ver Coisas',
            'mudanca_apetite': 'Mudança no Apetite',
            'mudanca_preferencia': 'Mudança de Preferência',
            'dificuldades_sono': 'Dificuldades no Sono',
            'movimentos_sono': 'Movimentos durante o Sono',
            'roncos': 'Roncos',
            'sonolencia_diurna': 'Sonolência Diurna',
        }
    }

    ordem_campos = {
        'pagina_1': [
            'dia',
            'doenca',
            'doenca_qual',
            'tratamento',
            'tratamento_qual',
            'pessoas',
            'relacao',
        ],
        'pagina_2': [
            'fuma',
            'bebe',
            'drogas',
            'remedios',
            'horas_sono',
            'insonia',
            'atividade',
            'frequencia',
        ],
        'pagina_3': [
            'diminuicao_tonus',
            'esquecimentos',
            'movimentos_faciais',
            'mudanca_humor',
            'perda_olfato',
            'qual_humor',
            'rigidez',
        ],
        'pagina_4': [
            'cialorreia',
            'deglutir',
            'dificuldade_mandibular',
            'diminuicao_tom',
            'gagueira',
            'lentidao_pronuncia',
            'pestanejar',
        ],
        'pagina_5': [
            'anotacoes_necessarias',
            'aprender_caminhos',
            'articular_palavras',
            'compreender_falado',
            'conversas_repetitivas',
            'desorientacao_temporal',
            'dificuldade_decisoes',
            'dificuldade_etapas',
            'dificuldade_localizar',
            'dificuldade_memoria',
            'dificuldade_palavras',
            'dificuldade_planejar',
            'dificuldade_praxias',
            'dificuldade_resolver',
            'dificuldade_vestir',
            'esquecimento_objetos',
            'esquecimentos_compromissos',
            'facilidade_distraicao',
            'momentos_confusos',
            'nomear_objetos',
            'perdido_caminhos',
        ],
        'pagina_6': [
            'atividades_basicas',
            'compras',
            'dificuldades_aivds',
            'humor_ira',
            'humor_isolamento',
            'humor_tristeza',
            'preparacao_refeicoes',
            'rendimento_trabalho',
        ],
        'pagina_7': [
            'agitacao_agressivo',
            'agitacao_ajuda',
            'agitacao_cooperativo',
            'agitacao_ritual',
            'ansiedade_preocupacao',
            'ansiedade_relaxar',
            'ansiedade_trivial',
            'apatia_engajamento',
            'apatia_indiferente',
            'apatia_interesse',
            'desinibicao_comportamento',
            'desinibicao_dizer',
            'desinibicao_impulsivo',
            'desinibicao_personalidade',
        ],
        'pagina_8': [
            'conversa_sozinho',
            'delirios',
            'dificuldades_sono',
            'mudanca_apetite',
            'mudanca_preferencia',
            'movimentos_sono',
            'ouvir_vozes',
            'roncos',
            'sonolencia_diurna',
            'ver_coisas',
        ],
    }




    if 'paciente_id' not in session:
        return redirect(url_for('cadastro.cadastro'))

    if request.method == 'POST':
        atendimento = session.get('atendimento')
        paciente_id = session.get('paciente_id')

        if not atendimento:
            flash('Nenhum atendimento a salvar.', 'error')
            return redirect(url_for('pagina_1.tela_pagina_1'))

        dados_json = json.dumps(atendimento)

        conn = sqlite3.connect(conexao_banco)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO atendimentos (paciente_id, dados) VALUES (?, ?)", (paciente_id, dados_json))
        conn.commit()
        conn.close()

        session.pop('atendimento', None)
        flash('Atendimento finalizado e salvo com sucesso!', 'success')
        return redirect(url_for('pagina_inicial'))  # ou outra página desejada

    # Método GET - mostra resumo para confirmar
    atendimento = session.get('atendimento', {})
    return render_template('pasta_consulta_medica/pagina_final.html', atendimento=atendimento, titulos=titulos_paginas, nomes_campos=nomes_campos, ordem_campos=ordem_campos)
