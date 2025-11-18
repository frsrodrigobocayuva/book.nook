import pytest
from app import create_app
from app.models import db

@pytest.fixture
def app():
    """Cria app com banco temporário."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente HTTP para testes."""
    return app.test_client()

@pytest.fixture
def logged_client(app):
    client = app.test_client()

    from app.models import User, db
    with app.app_context():
        user = User(username="tester", email="tester@test.com")
        user.set_password("SenhaFort3!")
        db.session.add(user)
        db.session.commit()

    # Faz login automático
    client.post("/login", data={
        "email": "tester@test.com",
        "password": "SenhaFort3!"
    })

    return client
