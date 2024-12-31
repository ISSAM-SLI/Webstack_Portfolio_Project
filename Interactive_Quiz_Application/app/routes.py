from app import app, db
import random
from questions import fetch_questions
from flask_login import login_required, current_user
from flask import request, redirect, url_for, session, render_template
from datetime import datetime
from app.models import QuizResult

@app.route('/')
def home():
        return 'Welcome to the Quiz App!'

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    """
    Route to display one question at a time.
    """
    # Initialize session data if not already present
    if 'questions' not in session:
        amount_of_questions = 5  # Set number of questions dynamically here
        session['questions'] = fetch_questions(amount=amount_of_questions)
        session['question_index'] = 0
        session['score'] = 0  # Initialize score

    # Get the stored questions and current question index
    questions = session['questions']
    question_index = session['question_index']

    # Ensure the index is within range of the number of questions
    if question_index >= len(questions):
        return redirect(url_for('result'))  # Redirect to results page when questions end

    question = questions[question_index]
    
    # Shuffle the answers for each question
    answers = question['incorrect_answers'] + [question['correct_answer']]
    random.shuffle(answers)

    # Handle form submission (user answering the question)
    if request.method == 'POST':
        selected_answer = request.form.get('answer')  # Get the answer chosen by the user
        correct_answer = question['correct_answer']
        
        # Check if the answer is correct
        if selected_answer == correct_answer:
            session['score'] += 1
        
        # Move to the next question
        session['question_index'] += 1
        return redirect(url_for('quiz'))  # Redirect to show the next question
    print("Question being sent to template:", question)

    return render_template(
        'quiz.html',
        question=question,
        answers=answers,
        question_index=question_index + 1,
        total_questions=len(questions)
    )
@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    """
    Route to handle quiz submissions and calculate score.
    """
    print(f"Reached submit_quiz route with score: {session.get('score', 0)} for user: {current_user.id}")
    score = session['score']
    print("Saving result:", score, "for user:", current_user.id)

    # Save the score to the database
    new_result = QuizResult(score=score, user_id=current_user.id, date_taken=datetime.utcnow())
    db.session.add(new_result)
    db.session.commit()

    return redirect(url_for('result', score=score))

@app.route('/result')
@login_required
def result():
    """
    Route to display quiz results after all questions are answered.
    """
    score = session.get('score', 0)  # Get the user's score from the session
    total_questions = 5  # Total number of questions
    session.clear()
    
    # Show the result page with the user's score
    return render_template('result.html', score=score, total_questions=total_questions)
