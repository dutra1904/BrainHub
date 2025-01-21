from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from models import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.senha == senha:
            session['user_id'] = usuario.id
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('home.home'))
        flash('E-mail ou senha incorretos!', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você foi desconectado com sucesso!', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('auth.cadastro'))
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('cadastro.html')
