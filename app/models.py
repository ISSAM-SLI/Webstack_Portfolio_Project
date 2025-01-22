from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """
    User model representing a user in the quiz application.
    
    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (int): The unique identifier for the user.
        username (str): The user's unique username.
        password (str): The user's password.
        email (str): The user's unique email address.
        quiz_results (QuizResult): A relationship storing the user's quiz results.
    """
    
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(150), unique=True, nullable=False)  # Unique username
    password = db.Column(db.String(150), nullable=False)  # User's password
    email = db.Column(db.String(150), unique=True, nullable=False)  # Unique email

    # One-to-many relationship with QuizResult
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)

    def __repr__(self):
        """
        String representation of the User object.
        
        Returns:
            str: Representation showing the user's username.
        """
        return f"<User {self.username}>"

class QuizResult(db.Model):
    """
    QuizResult model representing a user's quiz result.
    
    Attributes:
        id (int): The unique identifier for the quiz result.
        score (int): The score achieved by the user.
        date_taken (datetime): The date and time the quiz was taken.
        user_id (int): Foreign key linking the quiz result to the User.
    """
    
    id = db.Column(db.Integer, primary_key=True)  # Unique quiz result ID
    score = db.Column(db.Integer, nullable=False)  # Quiz score
    date_taken = db.Column(db.DateTime, nullable=False)  # Timestamp of quiz completion
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User

    def __repr__(self):
        """
        String representation of the QuizResult object.
        
        Returns:
            str: Representation showing the score and associated user ID.
            
        """
        return f"<QuizResult {self.score} for User {self.user_id}>"
