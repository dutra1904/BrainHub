from extensions import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    biografia = db.Column(db.Text, nullable=True)
    curso = db.Column(db.String(100), nullable=True)
    foto_perfil = db.Column(db.String(255), nullable=True)  # Nome do arquivo da foto
