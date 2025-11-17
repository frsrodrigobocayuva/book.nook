from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        """Gera o hash da senha e armazena no campo password_hash."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Compara uma senha digitada com o hash armazenado."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def set_email(self, email):
        self.email = email.strip().lower()


class Livro(db.Model):
    # __tablename__ define o nome da tabela no banco de dados.
    __tablename__ = 'livros'
    # Atributos que serão mapeados para colunas da tabela.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    authors = db.Column(db.String(120), nullable=False)
    publishedDate = db.Column(db.String(120), default=False)
    description = db.Column(db.String(8000), default=False)
    thumbnail = db.Column(db.String(4000), default=False)
    google_book_id = db.Column(db.String(50), nullable=False)