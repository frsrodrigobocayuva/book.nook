from flask import Blueprint, render_template, request, Response, redirect, url_for, jsonify, flash
from app.services.google_books import search_books, get_book_by_google_id
from app.models import Livro, db, User
from flask_login import login_user, logout_user, login_required, current_user

index_bp = Blueprint('Index', __name__)

@index_bp.route('/')
@login_required
def index():
    all_books = Livro.query.order_by(Livro.title).all()

    return render_template('shelf.html', results = all_books, user=current_user)

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

    existing_books = Livro.query.filter(Livro.google_book_id.in_(api_book_ids)).all()
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

        existing_book = Livro.query.filter_by(google_book_id=google_book_id).first()

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
                thumbnail=thumbnail
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
        google_book_id=book_id_to_remove
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

@index_bp.route('/book/<google_book_id>')
def book_detail(google_book_id):
    book = get_book_by_google_id(google_book_id)

    # Verifica se está na shelf
    saved_book = Livro.query.filter_by(google_book_id=google_book_id).first()

    book["in_shelf"] = saved_book is not None

    return render_template("ver.html", book=book)

@index_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        # Leitura dos campos do form
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        bio = request.form.get('bio', '').strip()

        # Validações simples — adapte conforme necessidade
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

    # GET -> renderiza o form com dados do usuário
    return render_template('user_edit.html', user=user)
