from flask import render_template, jsonify, request
from .question import fetch_quiz_questions
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

@app.route("/", methods=["GET"])
def get_quiz():
    """
    API Endpoint: Fetch and return quiz questions.
    URL Parameters:
        - amount: Number of questions (default: 5)
        - category: Category ID (optional)
        - difficulty: Difficulty level (optional)
    """
    amount = request.args.get("amount", default=5, type=int)
    category = request.args.get("category", default=None, type=str)
    difficulty = request.args.get("difficulty", default=None, type=str)

    questions = fetch_quiz_questions(amount, category, difficulty)
    return jsonify({"questions": questions})

@app.route("/question", methods=["GET"])
def get_quiz_question():
    """
    API Endpoint: Fetch a single quiz question.
    Includes time limit for answering.
    """
    question = fetch_quiz_questions(amount=1)[0]  # Fetch one question
    time_limit = 30  # Time limit in seconds per question
    return jsonify({"question": question, "time_limit": time_limit})