from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import random
import json
import os

app = Flask(__name__)
app.secret_key = 'segredo123'  # Necessário para sessões


# 🔹 Função para carregar dados JSON
def carregar_dados():
    try:
        caminho = os.path.join('detetive-logico', 'dados.json')
        with open(caminho, encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print('Arquivo dados.json não encontrado.')
        return {'personagens': [], 'locais': [], 'armas': []}


dados = carregar_dados()
personagens = dados['personagens']
locais = dados['locais']
armas = dados['armas']

def gerar_proposicoes(culpado, local, arma):
    proposicoes = []
    for personagem in personagens:
        props = []

        outro_personagem = random.choice([p for p in personagens if p != personagem])
        outro_local = random.choice([l for l in locais if l != local])
        outra_arma = random.choice([a for a in armas if a != arma])

        tipo = random.choice(['condicional', 'bicondicional', 'negacao'])

        if tipo == 'condicional':
            props.append(
                f"Se {outro_personagem} estava no {outro_local}, então a arma não foi {outra_arma}."
            )
        elif tipo == 'bicondicional':
            props.append(
                f"{personagem} é o culpado se, e somente se, estava no {local}."
            )
        elif tipo == 'negacao':
            props.append(
                f"Não é verdade que {outro_personagem} estava no {local}."
            )

        proposicoes.append({'personagem': personagem, 'proposicoes': props})

    return proposicoes

@app.route('/')
def index():
    return render_template('index.html',
                           personagens=personagens,
                           locais=locais,
                           armas=armas)

@app.route('/sorteio')
def sorteio():
    session['culpado'] = random.choice(personagens)
    session['local'] = random.choice(locais)
    session['arma'] = random.choice(armas)

    proposicoes = gerar_proposicoes(session['culpado'], session['local'], session['arma'])
    session['proposicoes'] = proposicoes

    return render_template('sorteio.html',
                           culpado=session['culpado'],
                           local=session['local'],
                           arma=session['arma'],
                           proposicoes=proposicoes)

@app.route('/proposicoes')
def proposicoes():
    proposicoes = session.get('proposicoes', [])
    return render_template('proposicoes.html', proposicoes=proposicoes)

@app.route('/debate')
def debate():
    return render_template('debate.html')

@app.route('/acusacao', methods=['GET', 'POST'])
def acusacao():
    if request.method == 'POST':
        acusacao = {
            'culpado': request.form['culpado'],
            'local': request.form['local'],
            'arma': request.form['arma']
        }
        session['acusacao'] = acusacao
        return redirect(url_for('resultado'))

    return render_template('acusacao.html',
                           personagens=personagens,
                           locais=locais,
                           armas=armas)

@app.route('/resultado')
def resultado():
    certo = 0
    acusacao = session.get('acusacao', {})

    if acusacao.get('culpado') == session['culpado']:
        certo += 1
    if acusacao.get('local') == session['local']:
        certo += 1
    if acusacao.get('arma') == session['arma']:
        certo += 1

    return render_template('resultado.html',
                           culpado=session['culpado'],
                           local=session['local'],
                           arma=session['arma'],
                           acerto=certo,
                           acusacao=acusacao)

@app.route('/gerar')
def gerar_caso():
    culpado = random.choice(personagens)
    local = random.choice(locais)
    arma = random.choice(armas)

    resultado = {
        'culpado': culpado,
        'local': local,
        'arma': arma
    }
    return jsonify(resultado)

@app.route('/espectador')
def espectador():
    return render_template('espectador.html',
                           jogadores=session.get('jogadores', []),
                           tempo_restante=session.get('tempo', 0),
                           fase_atual=session.get('fase', 'Sorteio'))


if __name__ == '__main__':
    app.run(debug=True)
