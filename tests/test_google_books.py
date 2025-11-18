from app.services.google_books import search_books

def test_google_books_service(monkeypatch, app):
    def fake_get(url, params):
        class FakeResponse:
            status_code = 200
            def json(self):
                return {
                    "items": [
                        {
                            "id": "TEST123",
                            "volumeInfo": {
                                "title": "Livro Fake",
                                "authors": ["Autor X"],
                                "publishedDate": "2000",
                                "description": "desc",
                                "imageLinks": {"thumbnail": "img"}
                            }
                        }
                    ]
                }
        return FakeResponse()

    monkeypatch.setattr("requests.get", fake_get)

    with app.app_context():
        result = search_books("teste")
        assert len(result) == 1
        assert result[0]["id"] == "TEST123"
