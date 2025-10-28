from flask import Blueprint, render_template, request, Response, redirect, url_for, jsonify
from app.services.google_books import search_books

index_bp = Blueprint('Index', __name__)

@index_bp.route('/')
def index():
    return render_template('index.html')

@index_bp.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Parâmetro 'q' é obrigatório"}), 400

    results = search_books(query)
    return jsonify(results)