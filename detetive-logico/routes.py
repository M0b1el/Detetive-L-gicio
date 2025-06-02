from flask import Flask, render_template, redirect, url_for, session, request
from tutorial_data import tutorial_casos
import time
app = Flask(__name__)
app.secret_key = 'segredo123'

# Tela de Carregamento
@app.route('/')
def loading():
    return render_template('loading.html')

# Home
@app.route('/home')
def home():
    return render_template('home.html')

# Modos de Jogo
@app.route('/modos')
def modos():
    return render_template('modos.html')

@app.route('/solo')
def solo():
    return render_template('solo.html')

# ---------------- Tutorial ----------------

# Início do tutorial
@app.route('/tutorial')
def tutorial_inicio():
    session['caso_atual'] = 0
    return redirect(url_for('tutorial_caso'))

# Página do caso atual
@app.route('/tutorial/caso')
def tutorial_caso():
    caso_atual = session.get('caso_atual', 0)

    if caso_atual >= len(tutorial_casos):
        return redirect(url_for('tutorial_conclusao'))

    caso = tutorial_casos[caso_atual]
    session['start_time'] = time.time()

    return render_template('tutorial/tutorial_caso.html', caso=caso)

# Verificar resposta
@app.route('/tutorial/verificar', methods=['POST'])
def tutorial_verificar():
    resposta = request.form.get('resposta')
    caso_atual = session.get('caso_atual', 0)
    caso = tutorial_casos[caso_atual]

    tempo_gasto = time.time() - session.get('start_time', time.time())
    tempo_restante = 180 - tempo_gasto

    if tempo_restante <= 0:
        return render_template('tutorial/tutorial_tempo_esgotado.html')

    if resposta.lower() == caso['culpado'].lower():
        session['caso_atual'] = caso_atual + 1
        return redirect(url_for('tutorial_caso'))
    else:
        return render_template(
            'tutorial/tutorial_erro.html',
            caso=caso,
            tempo_restante=int(tempo_restante)
        )

# Tutorial concluído
@app.route('/tutorial/concluido')
def tutorial_conclusao():
    return render_template('tutorial/tutorial_concluido.html')


if __name__ == '__main__':
    app.run(debug=True)
