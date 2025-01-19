from app import app, db
import random
from questions import fetch_questions
from flask_login import login_required, current_user
from flask import request, redirect, url_for, session, render_template
from datetime import datetime, timezone
from app.models import QuizResult

CATEGORY_MAP = {
    'General Knowledge': '9',
    'Computer': '18',
    'Mathematics': '19' ,
    'Sports': '21' ,
    'History': '23',
    'Art': '25',
    'Science & Nature': '17',
}

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
    """
    Quiz route: Displays one question at a time and processes user answers.

    """ 
    # Category selection step
    if 'questions' not in session or session['questions'] is None: 
        if request.method == 'POST':
            # Fetch user preferences from the form
            amount_of_questions = int(request.form.get('amount')) # Default to 5 questions
            category_name = request.form.get('category')  # Get selected category
            category_id = CATEGORY_MAP.get(category_name)
            difficulty = request.form.get('difficulty')  # Get selected difficulty

            # Store user preferences in the session
            session['amount'] = amount_of_questions
            session['category'] = category_name
            session['difficulty'] = difficulty

            # Fetch questions based on user preferences
            session['questions'] = fetch_questions(
                amount=amount_of_questions,
                category=category_id,
                difficulty=difficulty
            )
            session['question_index'] = 0
            session['score'] = 0  # Initialize score
            session['feedback'] = []  # Initialize feedback list

            return redirect(url_for('quiz'))  # Redirect to the quiz questions

        # Render category selection form
        return render_template('quiz_settings.html')

    questions = session['questions']
    question_index = session['question_index']
    answers = []

    # Quiz question rendering step
    if request.method == 'GET':
        if question_index >= len(questions):
            return redirect(url_for('submit_quiz'))
        question = questions[question_index]
        answers = question['incorrect_answers'] + [question['correct_answer']]
        random.shuffle(answers)
    # Handle form submission (user answering the question)
    elif request.method == 'POST':
        question_index = session['question_index'] 
        question = questions[question_index]
        # Shuffle the answers for each question
        answers = question['incorrect_answers'] + [question['correct_answer']]
        random.shuffle(answers)
        selected_answer = request.form.get('answer')
        correct_answer = question['correct_answer']

        # Check if the answer is correct and prepare feedback
        if selected_answer == correct_answer:
            session['score'] += 1
            feedback = "Correct!"
        else:
            feedback = f"Incorrect. The correct answer is: {correct_answer}"

        # Store feedback for each question
        session['feedback'].append({
            'question': question['question'],
            'selected_answer': selected_answer,
            'feedback': feedback
        })
        session['question_index'] += 1 # Move to the next question
        return redirect(url_for('quiz'))  # Redirect to show the next question

    return render_template(
        'quiz.html',
        question=question,
        answers=answers,
        index_question=session['question_index'],
        total_questions=len(session['questions']),
        amount=session.get('amount', 5),
        category=session.get('category', ''),
        difficulty=session.get('difficulty', '')
    )
@app.route('/submit_quiz', methods=['GET', 'POST'])
@login_required
def submit_quiz():
    """
    Submit quiz route: Handles quiz submission and saves the score.

    **Methods:** POST

    **Endpoint:** /submit_quiz

    **Responses:**
    - Saves the score and redirects to the results page.
    """
    score = session.get('score', 0)
    new_result = QuizResult(score=score, user_id=current_user.id, date_taken=datetime.now(timezone.utc))
    print(f"Saved QuizResult: {new_result}")
    db.session.add(new_result)
    db.session.commit()

    # Save the score temporarily for displaying the result
    session['last_score'] = score
    session['last_feedback'] = session.get('feedback', [])
    session['last_total_questions'] = len(session.get('questions', []))

    # Clear the session to reset quiz data
    session.pop('questions', None)
    session.pop('score', None)
    session.pop('feedback', None)
    session.pop('question_index', None)
    return redirect(url_for('result'))


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
    score = session.get('last_score', 0)
    total_questions = session.get('last_total_questions', 0)
    feedback = session.get('last_feedback', [])
    
    return render_template('result.html', score=score, total_questions=total_questions, feedback=feedback)