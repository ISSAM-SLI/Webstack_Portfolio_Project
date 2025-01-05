from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """User model representing a user of the quiz application.
    
    Attributes:
        id (int): The unique identifier for each user.
        username (str): The username of the user, unique and required.
        password (str): The password of the user, required.
        email (str): The email address of the user, unique and required.
        quiz_results (QuizResult): A relationship to store quiz results related to the user.
    """
    
    # Primary key for the user
    id = db.Column(db.Integer, primary_key=True)
    
    # The username of the user (unique and required)
    username = db.Column(db.String(150), unique=True, nullable=False)
    
    # The user's password (required)
    password = db.Column(db.String(150), nullable=False)
    
    # The user's email (unique and required)
    email = db.Column(db.String(150), unique=True, nullable=False)

    # Relationship: One-to-many relationship with QuizResult model
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)

    def __repr__(self):
        """Return a string representation of the User object.
        
        Returns:
            str: String representation of the user, displaying the username.
        """
        return f"<User {self.username}>"

class QuizResult(db.Model):
    """QuizResult model representing a user's quiz score.
    
    Attributes:
        id (int): The unique identifier for the quiz result.
        score (int): The score the user achieved on the quiz.
        date_taken (datetime): The date and time when the quiz was taken.
        user_id (int): The ID of the user who took the quiz, foreign key to User.
    """
    
    # Primary key for the quiz result
    id = db.Column(db.Integer, primary_key=True)
    
    # The score the user received on the quiz (required)
    score = db.Column(db.Integer, nullable=False)
    
    # The date and time when the quiz was taken (required)
    date_taken = db.Column(db.DateTime, nullable=False)
    
    # Foreign key relationship to the User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """Return a string representation of the QuizResult object.
        
        Returns:
            str: String representation of the quiz result, showing the score and user ID.
        """
        return f"<QuizResult {self.score} for User {self.user_id}>"
