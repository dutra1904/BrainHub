from flask import Flask
from config import Config
from extensions import db, migrate
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints
    register_blueprints(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Certifica-se de que as tabelas existam
    app.run(debug=True)
