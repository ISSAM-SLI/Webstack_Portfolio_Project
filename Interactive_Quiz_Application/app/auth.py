from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# Blueprint for authentication routes
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login.

    If the request method is POST, it checks the username and password against the database.
    If the credentials are valid, the user is logged in.
    """
    if request.method == 'POST':  # If form was submitted
        username = request.form['username']  # Retrieving the username
        password = request.form['password']  # Retrieving the password

        user = User.query.filter_by(username=username).first()  # Querying for the user by username
        if user:  # If user exists
            print("User found!")
            if check_password_hash(user.password, password):  # Verifying the password
                print("Password matches!")
                login_user(user)  # Log the user in
                return redirect(url_for('quiz'))  # Redirect to the quiz page
            else:
                print("Password does not match!")  # If password is incorrect
        else:
            return 'Invalid credentials, please try again.'  # If username is not found

    return render_template('login.html')  # Rendering the login page if GET request

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration.

    If the request method is POST, it creates a new user in the database with the provided username, password, and email.
    The password is hashed before storing.
    """
    if request.method == 'POST':  # If form was submitted
        username = request.form['username']  # Retrieving the username
        password = request.form['password']  # Retrieving the password
        email = request.form['email']  # Retrieving the email
        hashed_password = generate_password_hash(password)  # Hashing the password

        new_user = User(username=username, password=hashed_password, email=email)  # Creating new user instance
        db.session.add(new_user)  # Adding the new user to the database
        db.session.commit()  # Committing the session to save the user
        return redirect(url_for('auth.login'))  # Redirect to login page after registration

    return render_template('register.html')  # Rendering the registration page if GET request

@bp.route('/logout')
@login_required
def logout():
    """Log the user out.

    This route logs out the current logged-in user and redirects to the login page.
    """
    logout_user()  # Logging out the current user
    return redirect(url_for('auth.login'))  # Redirecting to login page after logout
