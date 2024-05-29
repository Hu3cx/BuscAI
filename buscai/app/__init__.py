from flask import Flask
app=Flask(__name__)
from buscai.app import routes
