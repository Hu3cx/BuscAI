from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from configparser import ConfigParser
from buscai.app.forms import LoginForm, RegistrationForm
from datetime import datetime

app = Flask(__name__)

# Configuração da chave secreta
app.config['SECRET_KEY'] = 'your_secret_key'

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ypy9zhue9bhgmkvu:dbss01rjyhubalta@gk90usy5ik2otcvi.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/znkk17si9stfyhdh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Carregar a configuração e inicializar o chatbot
config = ConfigParser()
config.read('credentials.ini')
api_key = config['gemini_ai']['API_KEY']

def get_chatbot_instance():
    from buscai.app.chatbot import ChatBot
    chatbot_instance = ChatBot(api_key=api_key, db=db)
    print(f"Chatbot instance: {chatbot_instance}")
    return chatbot_instance

# Modelo de usuário
class User(db.Model, UserMixin):
    __tablename__ = 'Usuarios'  # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    chatbot_instance = get_chatbot_instance()
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input.lower() == 'sair':
                logout_user()
                return redirect(url_for('login'))

        try:
            response = chatbot_instance.send_prompt(user_input, current_user)

        except Exception as e:
            response = f"Error: {e}"
        return render_template('index.html', user_input=user_input, response=response, chatbot=chatbot_instance)
    return render_template('index.html', chatbot=chatbot_instance)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = form.password.data  #função para hashear a senha
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Conta criada com sucesso! Você agora pode fazer login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Incorreto. Por favor verifique o usuário e senha informados', 'danger')
    return render_template('login.html', form=form)
 

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)

