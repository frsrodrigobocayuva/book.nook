from flask import *
from .blueprints.main.routes import *
from .auth import *
from app.config import Config
from dotenv import load_dotenv
from .models import db, bcrypt
from flask_login import LoginManager

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

    db.init_app(app)
    bcrypt.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'Auth.login'
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)

    return app