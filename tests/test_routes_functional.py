
def test_index_route(logged_client):
    resp = logged_client.get("/")
    assert resp.status_code == 200
    assert b"My Shelf" in resp.data or b"shelf" in resp.data


def test_search_route_with_results(logged_client, monkeypatch):
    fake_result = [{
        "id": "123",
        "title": "Livro Teste",
        "authors": "Autor X",
        "publishedDate": "2020",
        "thumbnail": None,
        "in_shelf": False
    }]

    def fake_search(query):
        return fake_result

    monkeypatch.setattr("app.services.google_books.search_books", fake_search)

    resp = logged_client.get("/search?q=teste")
    assert resp.status_code == 200

    assert b"Add to Shelf" in resp.data




def test_add_book_functional(logged_client):
    resp = logged_client.post("/add", data={
        "google_book_id": "abc123",
        "title": "Livro Adicionado",
        "authors": "Autor Y",
        "publishedDate": "2022",
        "thumbnail": ""
    }, follow_redirects=True)

    assert b"Livro adicionado com sucesso" in resp.data


def test_remove_book_functional(logged_client, app):
    from app.models import Livro, db
    with app.app_context():
        livro = Livro(
            google_book_id="del123",
            title="Excluir Livro",
            authors="Autor Z",
            publishedDate="2021",
            thumbnail=""
        )
        db.session.add(livro)
        db.session.commit()

    resp = logged_client.post("/remove_book", data={"google_book_id": "del123"}, follow_redirects=True)
    assert b"Livro removido da estante" in resp.data

