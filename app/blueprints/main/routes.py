from flask import Blueprint, render_template, request, Response, redirect, url_for, jsonify, flash
from app.services.google_books import search_books, get_book_by_google_id
from app.models import Livro, db, User
from flask_login import login_user, logout_user, login_required, current_user

index_bp = Blueprint('Index', __name__)

@index_bp.route('/')
@login_required
def index():
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

    return render_template('index.html', results=processed_results, user=current_user, active_page = "search")


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
            page_count = request.form.get('page_count', 0)

            new_book = Livro(
                google_book_id=google_book_id, 
                title=title,
                authors=authors,
                publishedDate=publishedDate,
                thumbnail=thumbnail,
                page_count=page_count,
                user_id=current_user.id
            )

            db.session.add(new_book)
            db.session.commit()
            flash('Livro adicionado com sucesso!', 'success')
        
        return redirect(request.referrer or url_for('Index.search'))

@index_bp.route('/book/<google_book_id>')
@login_required
def book_detail(google_book_id):
    saved_book = Livro.query.filter_by(google_book_id=google_book_id, user_id=current_user.id).first()

    book_data = {}

    if saved_book:
        book_data = {
            'id': saved_book.google_book_id,
            'title': saved_book.title,
            'authors': saved_book.authors,
            'publishedDate': saved_book.publishedDate,
            'thumbnail': saved_book.thumbnail,
            'page_count': saved_book.page_count,
            'current_page': saved_book.current_page,
            'in_shelf': True
        }

        api_data = get_book_by_google_id(google_book_id)
        book_data['description'] = api_data.get('description', '')
        
    else:
        book_data = get_book_by_google_id(google_book_id)
        book_data['in_shelf'] = False
        book_data['current_page'] = 0
        if 'pageCount' not in book_data:
            book_data['pageCount'] = 0

    return render_template("book_detail.html", book=book_data)

@index_bp.route('/update_progress', methods=['POST'])
@login_required
def update_progress():
    google_book_id = request.form.get('google_book_id')
    new_page = request.form.get('current_page')

    book = Livro.query.filter_by(google_book_id=google_book_id, user_id=current_user.id).first()
    
    if book and new_page:
        book.current_page = int(new_page)
        if book.page_count and book.current_page > book.page_count:
            book.current_page = book.page_count
            
        db.session.commit()
        flash('Progresso atualizado!', 'success')
    
    return redirect(url_for('Index.book_detail', google_book_id=google_book_id))
    
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

@index_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        bio = request.form.get('bio', '').strip()

        errors = []
        if not name:
            errors.append("Nome é obrigatório.")
        if not email:
            errors.append("E-mail é obrigatório.")

        if email and '@' not in email:
            errors.append("Formato de e-mail inválido.")

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('user_edit.html', user=user, flash_messages={'error': errors})

        user.name = name
        user.email = email
        user.bio = bio if bio else None

        try:
            db.session.commit()
            flash("Dados atualizados com sucesso.", "success")
            return redirect(url_for('Index.user_edit', user_id=user.id))
        except Exception as ex:
            db.session.rollback()
            flash("Ocorreu um erro ao salvar. Tente novamente.", "error")
            return render_template('user_edit.html', user=user, flash_messages={'error': ["Erro ao salvar."]})

    return render_template('user_edit.html', user=user)
