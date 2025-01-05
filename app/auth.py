from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# Blueprint for authentication routes
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('quiz'))
            else:
                # Password is incorrect
                return render_template('login.html', error="Incorrect password. Please try again.")
        else:
            # Username does not exist
            return render_template('login.html', error="Username not found. Please register first.")

    return render_template('login.html')
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Username already exists. Please choose a different one.")
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error="Email already registered. Please use a different email.")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('register.html')
@bp.route('/logout')
@login_required
def logout():
    """Log the user out.

    This route logs out the current logged-in user and redirects to the login page.
    """
    logout_user()  # Logging out the current user
    return redirect(url_for('auth.login'))  # Redirecting to login page after logout
