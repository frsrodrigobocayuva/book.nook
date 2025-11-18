def test_index_route(client):
    resp = client.get("/", follow_redirects=True)
    assert resp.status_code == 200

def test_search_route_empty_query(client):
    resp = client.get("/search?q=", follow_redirects=True)
    assert resp.status_code == 200

def test_add_book_route(client, app):
    with app.app_context():
        data = {
            "google_book_id": "XYZ123",
            "title": "Livro Teste",
            "authors": "Autor Teste",
            "publishedDate": "2020",
            "thumbnail": "http://exemplo.com/img.png"
        }
        resp = client.post("/add", data=data)
        assert resp.status_code in (302, 301)

def test_remove_book_route(client, app):
    with app.app_context():
        from app.models import Livro, db

        livro = Livro(
            google_book_id="AAA111",
            title="Teste",
            authors="Autor",
            publishedDate="2020",
            thumbnail=""
        )
        db.session.add(livro)
        db.session.commit()

        resp = client.post("/remove_book", data={"google_book_id": "AAA111"})
        assert resp.status_code in (302, 301)
