
def test_login_invalido(client, app):
    from app.models import User, db
    with app.app_context():
        user = User(username="teste", email="teste@example.com")
        user.set_password("SenhaFort3!")
        db.session.add(user)
        db.session.commit()

    resp = client.post("/login", data={
        "email": "teste@example.com",
        "password": "Errada123"
    }, follow_redirects=True)

    assert resp.status_code == 200
    assert b"Invalid email or password" in resp.data


def test_login_valido(client, app):
    from app.models import User, db
    with app.app_context():
        user = User(username="user", email="user@test.com")
        user.set_password("StrongPass1!")
        db.session.add(user)
        db.session.commit()

    resp = client.post("/login", data={
        "email": "user@test.com",
        "password": "StrongPass1!"
    }, follow_redirects=True)

    assert resp.status_code == 200
    assert b"Logged in successfully" in resp.data


def test_registro_senha_fraca(client):
    resp = client.post("/register", data={
        "email": "novo@test.com",
        "username": "usuario",
        "password": "123",
        "passwordConfirmation": "123"
    }, follow_redirects=True)

    assert resp.status_code == 200
    assert b"Password too weak" in resp.data


def test_registro_valido(client):
    resp = client.post("/register", data={
        "email": "novo@teste.com",
        "username": "novoUser",
        "password": "SenhaFort3!",
        "passwordConfirmation": "SenhaFort3!"
    }, follow_redirects=True)

    assert resp.status_code == 200
    assert b"Account created successfully" in resp.data


def test_logout(client, app):
    from app.models import User, db
    with app.app_context():
        user = User(username="x", email="x@x.com")
        user.set_password("SenhaFort3!")
        db.session.add(user)
        db.session.commit()

    client.post("/login", data={
        "email": "x@x.com",
        "password": "SenhaFort3!"
    })

    resp = client.get("/logout", follow_redirects=True)

    assert resp.status_code == 200
    assert b"You have been logged out" in resp.data
