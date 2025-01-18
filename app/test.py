from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do Banco de Dados (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'  # Necessário para usar o flash
db = SQLAlchemy(app)

# Modelo do Banco de Dados
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

# Criação do banco de dados
with app.app_context():
    db.create_all()

# Página inicial
@app.route('/')
def home():
    return "Bem-vindo ao sistema! <a href='/login'>Faça Login</a> ou <a href='/cadastro'>Cadastre-se</a>"

# Página de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        # Verifica se o usuário existe no banco de dados
        usuario = Usuario.query.filter_by(email=email, senha=senha).first()
        
        if usuario:
            return redirect(url_for('home'))  # Redireciona para a página inicial
        else:
            flash('E-mail ou senha inválidos. Tente novamente!', 'danger')
    
    return render_template('login.html')

# Página de Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        # Verifica se o e-mail já está cadastrado
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado. Tente outro!', 'danger')
            return redirect(url_for('cadastro'))

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))  # Redireciona para a página de login
    
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
