from buscai.app import app  # Importa o objeto 'app' do módulo 'app'

@app.route('/')
def index():
    return render_template('index.html')
