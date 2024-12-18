from flask import Blueprint, render_template, redirect, url_for, request, json, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, users_db  # Assuming you've created a User model
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Mock user database

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_db.get(username)
        #print(f"Retrieved user: {user}")
        #print(f"Stored hashed password: {user.password}")

        if user:
            print("User found!")
            if check_password_hash(user.password, password):
                print("Password matches!")
                login_user(user)
                print(users_db)
                return redirect(url_for('dashboard'))
            else:
                print("Password does not match!")
        else:
            print(f"Invalid login attempt for {username}")
            return json('Invalid credentials, please try again.')

    return json (render_template('login.html'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username in users_db or any(user.email == email for user in users_db.values()):
            flash('Username or email already exists. Please choose a different username or email.')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)  # Hash the password
        # Create new user
        new_user = User(id=username, username=username, email=email, password=hashed_password)
        users_db[username] = new_user

        flash('User registered successfully!')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()  # Log the user out
    return redirect(url_for('auth.login'))
