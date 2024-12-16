from flask import render_template
from flask_login import login_required, current_user
from app  import app

@app.route('/')
def home():
        return 'Welcome to the Quiz App!'
@app.route('/dashboard')
@login_required
def dashboard():
    #print(f"Current User: {current_user.get_id()}")
    return f"Hello,! Welcome {current_user.username} to your quiz dashboard."
