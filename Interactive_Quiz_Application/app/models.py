from app import db
from flask_login import UserMixin

# User model for storing user information
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    # Relationship with QuizResult model
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

# QuizResult model for storing the results of each quiz attempt
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for the quiz result
    score = db.Column(db.Integer, nullable=False)  # User score for the quiz
    date_taken = db.Column(db.DateTime, nullable=False)  # Date when the quiz was taken
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User table

    def __repr__(self):
        return f"<QuizResult {self.score} for User {self.user_id}>"

