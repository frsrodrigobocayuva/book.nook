import requests
from flask import current_app

def search_books(query, max_results=25) -> list:
    """Busca livros usando a API do Google Books."""
    api_key = current_app.config.get("GOOGLE_BOOKS_API_KEY")
    base_url = "https://www.googleapis.com/books/v1/volumes"

    params = {
        "q": query,
        "maxResults": max_results,
        "key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        return {"error": f"Erro na requisição: {response.status_code}"}

    data: dict = response.json()

    books: list[dict] = []
    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})
        books.append({
            "id": item.get("id"),
            "title": volume_info.get("title"),
            "authors": "Sem informações de autor" if ', '.join(volume_info.get("authors", [])) == "" else ', '.join(volume_info.get("authors", [])),
            "publishedDate": volume_info.get("publishedDate"),
            "description": volume_info.get("description"),
            "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
            "pageCount": volume_info.get("pageCount", 100), 
            "in_shelf": False
        })
    return books

def get_book_by_google_id(google_book_id) -> dict | None:
    """Busca um único livro pelo Google Book ID."""
    api_key = current_app.config.get("GOOGLE_BOOKS_API_KEY")
    base_url = f"https://www.googleapis.com/books/v1/volumes/{google_book_id}"

    params = {
        "key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        return None

    data: dict = response.json()
    volume_info = data.get("volumeInfo", {})

    book = {
        "id": data.get("id"),
        "title": volume_info.get("title"),
        "authors": "Sem informações de autor" if not volume_info.get("authors") else ', '.join(volume_info.get("authors")),
        "publishedDate": volume_info.get("publishedDate"),
        "description": volume_info.get("description"),
        "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
        "pageCount": volume_info.get("pageCount", 100),
        "in_shelf": False
    }

    return book