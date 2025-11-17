from flask import Blueprint, render_template, request, Response, redirect, url_for, jsonify, flash
from app.services.google_books import search_books
from app.models import Livro, db
from flask_login import login_user, logout_user, login_required, current_user

index_bp = Blueprint('Index', __name__)

@index_bp.route('/')
@login_required
def index():
    #all_books = Livro.query.order_by(Livro.title).all()
    user_books = Livro.query.filter_by(user_id=current_user.id).order_by(Livro.title).all()

    return render_template('shelf.html', results = user_books, user=current_user)

@index_bp.route("/search")
@login_required
def search():
    query = request.args.get("q")
    if not query:
        return render_template('index.html', results=[])

    api_results = search_books(query)
    
    if not api_results:
        return render_template('index.html', results=[])

    api_book_ids = [book['id'] for book in api_results if 'id' in book]

    existing_books = Livro.query.filter(Livro.google_book_id.in_(api_book_ids), Livro.user_id == current_user.id).all()
    shelf_ids = {book.google_book_id for book in existing_books}

    processed_results = []
    for book_data in api_results:
        if 'id' in book_data:
            book_data['in_shelf'] = book_data['id'] in shelf_ids
            processed_results.append(book_data)

    return render_template('index.html', results=processed_results, user=current_user)

@index_bp.route('/add', methods=['POST'])
@login_required
def add_book():
    if request.method == 'POST':
        google_book_id = request.form['google_book_id']

        existing_book = Livro.query.filter_by(google_book_id=google_book_id, user_id=current_user.id).first()

        if existing_book:
            flash('Este livro já está na sua estante!', 'warning')
        else:
            title = request.form['title']
            authors = request.form['authors']
            publishedDate = request.form['publishedDate']
            thumbnail = request.form['thumbnail']

            new_book = Livro(
                google_book_id=google_book_id, 
                title=title,
                authors=authors,
                publishedDate=publishedDate,
                thumbnail=thumbnail,
                user_id=current_user.id
            )

            db.session.add(new_book)
            db.session.commit()
            flash('Livro adicionado com sucesso!', 'success')
        
        return redirect(request.referrer or url_for('Index.search'))
    
@index_bp.route('/remove_book', methods=['POST'])
@login_required
def remove_book():
    book_id_to_remove = request.form.get('google_book_id')
    
    book_in_shelf = Livro.query.filter_by(
        google_book_id=book_id_to_remove, user_id=current_user.id
    ).first()
    
    if book_in_shelf:
        try:
            db.session.delete(book_in_shelf)
            db.session.commit()
            flash('Livro removido da estante.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao remover o livro: {e}', 'danger')
    else:
        flash('Livro não encontrado na sua estante.', 'warning')

    return redirect(request.referrer or url_for('Index.search'))