from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Carregar dados.json
caminho_arquivo = os.path.join(os.path.dirname(__file__), 'data', 'dados.json')
with open(caminho_arquivo, 'r', encoding='utf-8') as f:
    dados = json.load(f)

@app.route('/tutorial/<int:caso_id>')
def jogar_tutorial(caso_id):
    # Carrega dados do JSON
    with open('dados.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)

    # Busca o caso pelo ID
    caso = next((c for c in dados['tutoriais'] if c['id'] == caso_id), None)
    if not caso:
        return "Caso não encontrado", 404

    # Geração de proposições didáticas fixas por enquanto (você pode customizar depois)
    dicas_gerais = {
        1: "Alguém mentiu sobre onde estava o gato. Observe o local e quem pode manipulá-lo.",
        2: "O bolo estava na cozinha. Quem esteve lá sem justificativa?",
        3: "O ladrão sabia exatamente qual livro levar. Quem conhece os segredos da biblioteca?"
    }

    proposicoes_geradas = [
        f"{caso['culpado']} foi visto perto da {caso['local']}.",
        f"Um dos suspeitos afirmou que {caso['culpado']} estava agindo estranho.",
        "A arma do crime foi encontrada próxima à cena.",
        "Nem todos os suspeitos têm um álibi confirmado.",
        "O verdadeiro culpado tentou disfarçar sua culpa com uma falsa acusação."
    ]

    caso['proposicoes'] = proposicoes_geradas
    caso['dica'] = dicas_gerais.get(caso_id, "Use sua lógica para eliminar os inocentes.")

    return render_template('jogo.html', caso=caso, personagem={}, modo='tutorial')

# ------------------- Rotas -------------------

# Loading
@app.route('/')
def loading():
    return render_template('loading.html')

# Home
@app.route('/home')
def home():
    return render_template('home.html')

# Modos
@app.route('/modos')
def modos():
    return render_template('modos.html')

# Tutorial - lista de casos
@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html', tutoriais=dados['tutoriais'])

# Tutorial - detalhe do caso
@app.route('/tutorial-caso/<int:id>')
def tutorial_caso(id):
    caso = dados['tutoriais'][id - 1]
    return render_template('tutorial_caso.html', caso=caso)

# Seleção de personagem para tutorial
@app.route('/selecionar-personagem/<int:id>')
def selecionar_personagem(id):
    caso = dados['tutoriais'][id - 1]
    personagens = dados['personagens']
    destino = url_for('jogar', id=id)
    return render_template('selecionar_personagem.html', caso=caso, personagens=personagens, destino=destino)

# Jogar tutorial
@app.route('/tutorial-caso/<int:id>/jogar')
def jogar(id):
    personagem = request.args.get('personagem')
    caso = dados['tutoriais'][id - 1]
    return render_template('jogo.html', caso=caso, personagem=personagem, armas=dados['armas'])

# Solo - seleção de personagem (sem caso)
@app.route('/solo/selecionar-personagem')
def selecionar_personagem_solo():
    personagens = dados['personagens']
    destino = url_for('jogo_solo')
    return render_template('selecionar_personagem.html', caso=None, personagens=personagens, destino=destino)

# Solo - jogo livre
@app.route('/solo/jogo')
def jogo_solo():
    personagem = request.args.get('personagem')
    return render_template('jogo.html', personagem=personagem, caso=None, armas=dados['armas'])

# Multiplayer
@app.route('/multiplayer')
def multiplayer():
    return render_template('multiplayer.html')

# (opcional) função para recarregar os dados se quiser usar depois
def carregar_dados():
    caminho = os.path.join(os.path.dirname(__file__), 'data', 'dados.json')
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)
