from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'd28ebc859848fe4f6b9154bffefdc230'

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

from app import error_404
# User loader for Flask-Login
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    """Retrieve user by ID for Flask-Login."""
    return User.query.get(int(user_id))

# Register blueprints
from . import routes, auth
app.register_blueprint(auth.bp)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()
