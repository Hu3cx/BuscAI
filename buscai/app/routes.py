from buscai.app.app import app
# Arquivo: routes.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/buscai/app/templates/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
