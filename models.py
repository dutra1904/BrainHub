from extensions import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    biografia = db.Column(db.Text, nullable=True)
    curso = db.Column(db.String(100), nullable=True)
    foto_perfil = db.Column(db.String(255), nullable=True)  # Nome do arquivo da foto

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    perguntas = db.relationship('Pergunta', backref='quizzes', cascade='all, delete-orphan')

class Pergunta(db.Model):
    __tablename__ = 'perguntas'

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'escrever' ou 'marcar'
    resposta_correta = db.Column(db.String(200), nullable=False)
    opcoes = db.Column(db.String(500), nullable=True)  # Armazena as opções separadas por vírgula
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)