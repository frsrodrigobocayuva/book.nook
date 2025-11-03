from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Livro(db.Model):
    # __tablename__ define o nome da tabela no banco de dados.
    __tablename__ = 'livros'
    # Atributos que serão mapeados para colunas da tabela.
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    authors = db.Column(db.String(120), nullable=False)
    publishedDate = db.Column(db.String(120), default=False)
    description = db.Column(db.String(8000), default=False)
    thumbnail = db.Column(db.String(4000), default=False)
    google_book_id = db.Column(db.String(50), unique=True, nullable=False)