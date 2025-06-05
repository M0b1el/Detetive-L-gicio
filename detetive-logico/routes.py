from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Carregar dados.json
caminho_arquivo = os.path.join(os.path.dirname(__file__), 'data', 'dados.json')
with open(caminho_arquivo, 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Rota Loading
@app.route('/')
def loading():
    return render_template('loading.html')

# Rota Home
@app.route('/home')
def home():
    return render_template('home.html')

# Rota Modos 
@app.route('/modos')
def modos():
    return render_template('modos.html')

#  Rota tutorial 
@app.route('/tutorial')
def tutorial():
    # Página com lista dos tutoriais
    return render_template('tutorial.html', tutoriais=dados['tutoriais'])

@app.route('/tutorial-caso/<int:id>')
def tutorial_caso(id):
    # Página de descrição do caso
    caso = dados['tutoriais'][id - 1]
    return render_template('tutorial_caso.html', caso=caso)

@app.route('/tutorial-caso/<int:id>/personagem')
def selecionar_personagem(id):
    # Página de seleção de personagem
    caso = dados['tutoriais'][id - 1]
    personagens = dados['personagens']
    return render_template('selecionar_personagem.html', caso=caso, personagens=personagens)

@app.route('/tutorial-caso/<int:id>/jogar')
def jogar(id):
    personagem = request.args.get('personagem')
    caso = dados['tutoriais'][id - 1]
    return render_template('jogo.html', caso=caso, personagem=personagem)

# Rota Solo
@app.route('/solo')
def solo():
    return render_template('solo.html')

# Rota Multiplayer 
@app.route('/multiplayer')
def multiplayer():
    return render_template('multiplayer.html')

# carregando dados 
def carregar_dados():
    caminho = os.path.join(os.path.dirname(__file__), 'data', 'dados.json')
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

