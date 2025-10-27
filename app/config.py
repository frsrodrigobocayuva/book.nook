import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
