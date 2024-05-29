from flask import Flask

app = Flask(__name__)

# Importar o módulo de rotas para registrar os endpoints
from buscai.app import routes
