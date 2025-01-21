from routes.home import home_bp
from routes.perfil import perfil_bp
from routes.auth import auth_bp
from routes.quizzes import quizzes_bp

def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(quizzes_bp)