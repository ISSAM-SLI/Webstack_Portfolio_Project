from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError 
from app import db
import re

# Blueprint for authentication routes
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Function used to Login a user.

    **Methods:** GET, POST

    **Endpoint:** /auth/login

    **Request Parameters:**
    - `username` (form data): The username of the user attempting to log in.
    - `password` (form data): The password of the user.

    **Responses:**
    - GET: Render the login page.
    - POST:
        - Redirect to the quiz page if login is successful.
        - Render the login page with an error message if credentials are invalid.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('quiz'))
            else:
                return render_template('login.html', error="Incorrect password. Please try again.")
        else:
            return render_template('login.html', error="Username not found. Please register first.")

    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user.

    **Methods:** GET, POST

    **Endpoint:** /auth/register

    **Request Parameters:**
    - `username` (form data): The desired username.
    - `password` (form data): The desired password.
    - `email` (form data): The user's email address.

    **Responses:**
    - GET: Render the registration page.
    - POST:
        - Redirect to the login page upon successful registration.
        - Render the registration page with an error if the username or email is already taken.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

         #This line will Validate password complexity (check for numbers- length, special characters)
        if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[A-Za-z]", password):
            return render_template('register.html', error="Password must be at least 8 characters, including both letters and numbers.")

        try:
            validate_email(email)  # This Will raise an exception if invalid email
        except EmailNotValidError as e:
            return render_template('register.html', error="Please provide a valid email address.")

        #  This will Check if username or email already exists in the database
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Username already exists. Please choose a different one.")
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error="Email already registered. Please use a different email.")
        
        # Hashing the password to store it in the database
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)
        # Adding the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    """
    Log out the current user.

    **Methods:** GET

    **Endpoint:** /auth/logout

    **Responses:**
    - Redirect to the login page after successfully logging out.
    """
    logout_user()  # Logging out the current user
    return redirect(url_for('auth.login'))  # Redirecting to login page after logout
