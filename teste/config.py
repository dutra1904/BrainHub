import os

class Config:
    SECRET_KEY = 'chave-secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///usuarios.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
