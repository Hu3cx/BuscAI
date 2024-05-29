from flask import Flask, request, render_template, redirect, url_for
from configparser import ConfigParser
from buscai.app.chatbot import chatBot


app = Flask(__name__)

# Carregar a configuração e inicializar o chatbot
config = ConfigParser()
config.read('credentials.ini')
api_key = config['gemini_ai']['API_KEY']
chatbot_instance = chatBot(api_key=api_key)  # Renomear para evitar conflito de nomes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input.lower() == 'sair':
            return redirect(url_for('goodbye'))
        try:
            response = chatbot_instance.send_prompt(user_input)
        except Exception as e:
            response = f"Error: {e}"
        return render_template('index.html', user_input=user_input, response=response, chatbot=chatbot_instance)
    return render_template('index.html', chatbot=chatbot_instance)

@app.route('/goodbye')
def goodbye():
    return "Saindo..."

if __name__ == '__main__':
    app.run(debug=True)
