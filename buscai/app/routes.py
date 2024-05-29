from buscai.app.app import app
from flask import render_template

@app.route('/')
def home():
    return render_template('index.html')

@app.route('buscai/app/templates/index')
def index():
    return render_template('index.html')
