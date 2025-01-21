from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from extensions import db
from models import Usuario
import os

perfil_bp = Blueprint('perfil', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@perfil_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar o perfil!', 'danger')
        return redirect(url_for('auth.login'))
    
    usuario = Usuario.query.get(session['user_id'])
    if not usuario:
        flash('Usuário não encontrado!', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.biografia = request.form['biografia']
        usuario.curso = request.form['curso']

        if 'foto_perfil' in request.files:
            foto = request.files['foto_perfil']
            if foto and allowed_file(foto.filename):
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                usuario.foto_perfil = filename

        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('perfil.perfil'))

    return render_template('perfil.html', usuario=usuario)
