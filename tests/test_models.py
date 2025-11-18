from app.models import Livro, db

def test_model_criacao(app):
    with app.app_context():
        livro = Livro(
            google_book_id="ID123",
            title="Titulo",
            authors="Autor",
            publishedDate="2023",
            thumbnail=""
        )

        db.session.add(livro)
        db.session.commit()

        salvo = Livro.query.first()
        assert salvo.title == "Titulo"
