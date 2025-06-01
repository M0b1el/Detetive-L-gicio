from flask import Flask, render_template, redirect, url_for, session
import random
import json
import os
import time 

app = Flask(__name__)
app.secret_key = 'segredo123'

# Tela de Carregamento
@app.route('/')
def loading():
    return render_template('loading.html')

# Tela Home
@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
