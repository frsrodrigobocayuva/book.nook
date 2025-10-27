from flask import *
from .blueprints.main.routes import *

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hello.db'
    # db.init_app(app)

    # with app.app_context():
    #     db.create_all()

    app.register_blueprint(index_bp)
    # app.register_blueprint(name_bp)
    
    return app