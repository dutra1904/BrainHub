from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'chave-secreta'  # Necessário para usar sessões
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

# Página Home (após login)
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# Página Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        # Verifica se o usuário existe
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.senha == senha:
            session['user_id'] = usuario.id  # Armazena o ID do usuário na sessão
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('home'))  # Redireciona para a página home
        else:
            flash('E-mail ou senha incorretos!', 'danger')
    
    return render_template('login.html')

# Rota Logout (Sair)
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove o usuário da sessão
    flash('Você foi desconectado com sucesso!', 'info')
    return redirect(url_for('login'))  # Redireciona para a página de login

# Página de Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado. Tente outro!', 'danger')
            return redirect(url_for('cadastro'))
        
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

if __name__ == '__main__':
    db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)
