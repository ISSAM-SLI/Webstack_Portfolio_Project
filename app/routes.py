from app import app, db
import random
from questions import fetch_questions
from flask_login import login_required, current_user
from flask import request, redirect, url_for, session, render_template
from datetime import datetime
from app.models import QuizResult

@app.route('/')
def home():
        """
    Home route.

    **Methods:** GET

    **Endpoint:** /

    **Responses:**
    - Display a welcome message for the Quiz App.
    """
        return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    print("Quiz route called")
    """
    Quiz route: Displays one question at a time and processes user answers.

    **Methods:** GET, POST

    **Endpoint:** /quiz

    **Session Variables:**
    - `questions`: List of questions fetched for the quiz.
    - `question_index`: Current index of the question being displayed.
    - `score`: Current score of the user.
    - `feedback`: List of feedback for each answered question.

    **Responses:**
    - GET: Renders the next question with answer choices.
    - POST: Processes the user's answer and updates session data.
      - Redirects to the next question if available.
      - Redirects to the results page if all questions are completed.
    """
    if 'questions' not in session:
        amount_of_questions = 5
        session['questions'] = fetch_questions(amount=amount_of_questions)
        session['question_index'] = 0
        session['score'] = 0
        session['feedback'] = []

    questions = session['questions']
    question_index = session['question_index']

    if question_index >= len(questions):
        return redirect(url_for('result'))

    question = questions[question_index]
    
    answers = question['incorrect_answers'] + [question['correct_answer']]
    random.shuffle(answers)

    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        correct_answer = question['correct_answer']
        
        if selected_answer == correct_answer:
            session['score'] += 1
            feedback = "Correct!"
        else:
            feedback = f"Incorrect. The correct answer is: {correct_answer}"
        
        session['feedback'].append({
            'question': question['question'],
            'selected_answer': selected_answer,
            'feedback': feedback
        })
        session['question_index'] += 1
        return redirect(url_for('quiz'))

    return render_template(
        'quiz.html',
        question=question,
        answers=answers,
        index_question=question_index + 1,
        total_questions=len(questions)
    )
@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    print("Submit Quiz route called")
    """
    Submit quiz route: Handles quiz submission and saves the score.

    **Methods:** POST

    **Endpoint:** /submit_quiz

    **Responses:**
    - Saves the score and redirects to the results page.
    """
    score = session['score']
    new_result = QuizResult(score=score, user_id=current_user.id, date_taken=datetime.utcnow())
    print(f"Saved QuizResult: {new_result}")
    db.session.add(new_result)
    db.session.commit()

    return redirect(url_for('result', score=score))

@app.route('/result')
@login_required
def result():
    """
    Result route: Displays the quiz results and feedback.

    **Methods:** GET

    **Endpoint:** /result

    **Responses:**
    - Renders the result page with:
      - Final score
      - Total questions
      - Feedback on each answered question.
    """
    score = session.get('score', 0)
    total_questions = 5
    feedback = session.get('feedback', [])
    session.clear()
    
    return render_template('result.html', score=score, total_questions=total_questions, feedback=feedback)

