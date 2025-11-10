from flask import Blueprint, flash, render_template, redirect, request, url_for
import re
from app.models import User, db
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('Auth', __name__)

def is_valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email)

def is_valid_username(username):
    pattern = r"^(?![_.])(?!.*[_.]{2})[A-Za-z0-9._]{3,20}(?<![_.])$"
    return re.match(pattern, username)

def is_strong_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
    return re.match(pattern, password)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            flash("Logged in successfully! 🎉", category="success")
            login_user(user, remember=True)
            return redirect(url_for('main.index'))
        else:
            flash("Invalid email or password. Please try again.", category="error")

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", category="success")
    return redirect(url_for('Auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('passwordConfirmation')

        errors = []  # lista para acumular mensagens de erro

        if User.query.filter_by(email=email).first():
            errors.append("Email already registered.")
        if User.query.filter_by(username=username).first():
            errors.append("Username already taken.")

        if not is_valid_email(email):
            errors.append("Invalid email format.")

        if not is_valid_username(username):
            errors.append("Invalid username. Use 3 to 20 characters: letters, numbers, dots, or underscores only.")

        if not is_strong_password(password):
            errors.append("Password too weak. Must include upper, lower, number, and symbol.")

        if password != password_confirm:
            errors.append("Passwords do not match.")

        if errors:
            for msg in errors:
                flash(msg, category="error")
            return render_template('register.html', email=email, username=username)

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! 🎉", category="success")
        return redirect(url_for('Auth.login'))

    return render_template('register.html')