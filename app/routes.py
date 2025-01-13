from app import app, db
import random
from questions import fetch_questions
from flask_login import login_required, current_user
from flask import request, redirect, url_for, session, render_template
from datetime import datetime
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
    Route to display category selection first and then proceed to the quiz.
    """
    if 'questions' not in session or session['questions'] is None:  # Category selection step
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

    # Quiz question rendering step
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
        # Move to the next question
        session['question_index'] += 1
        return redirect(url_for('quiz'))  # Redirect to show the next question

    return render_template(
        'quiz.html',
        question=question,
        answers=answers,
        index_question=question_index + 1,
        total_questions=len(questions),
        amount=session.get('amount', 5),
        category=session.get('category', ''),
        difficulty=session.get('difficulty', '')
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

