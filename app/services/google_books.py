import requests
from flask import current_app

def search_books(query, max_results=10):
    api_key = current_app.config.get("GOOGLE_BOOKS_API_KEY")
    base_url = "https://www.googleapis.com/books/v1/volumes"

    params = {"q": query, "maxResults": max_results}
    if api_key:
        params["key"] = api_key

    try:
        resp = requests.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Erro na requisição: {e}"}

    data = resp.json()
    items = data.get("items", [])
    books = []
    for item in items:
        vi = item.get("volumeInfo", {})
        image_links = vi.get("imageLinks") or {}
        books.append({
            "id": item.get("id"),
            "title": vi.get("title"),
            "authors": vi.get("authors", []),
            "publisher": vi.get("publisher"), 
            "publishedDate": vi.get("publishedDate"),
            "description": vi.get("description"),
            "thumbnail": image_links.get("thumbnail")
        })
    return books
