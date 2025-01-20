from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'chave-secreta'  # Necessário para usar sessões
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Diretório para salvar as fotos de perfil
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Tipos de arquivos permitidos
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    biografia = db.Column(db.Text, nullable=True)
    curso = db.Column(db.String(100), nullable=True)
    foto_perfil = db.Column(db.String(255), nullable=True)  # Campo para armazenar o nome do arquivo da foto

# Função para verificar se o arquivo é uma imagem permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Página Home (após login)
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# Página Perfil
@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar o perfil!', 'danger')
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get(session['user_id'])

    if usuario is None:
        flash('Usuário não encontrado!', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Atualizar os dados do perfil
        usuario.nome = request.form['nome']
        usuario.biografia = request.form['biografia']
        usuario.curso = request.form['curso']

        # Verificar se uma foto foi enviada
        if 'foto_perfil' in request.files:
            foto = request.files['foto_perfil']
            if foto and allowed_file(foto.filename):
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                usuario.foto_perfil = filename

        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('perfil'))
    
    return render_template('perfil.html', usuario=usuario)

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
        
        # Verifica se o e-mail já foi cadastrado
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado. Tente outro!', 'danger')
            return redirect(url_for('cadastro'))
        
        # Cria um novo usuário
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))  # Redireciona para o login
    
    return render_template('cadastro.html')

if __name__ == '__main__':
    db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)
