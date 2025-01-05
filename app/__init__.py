from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'd28ebc859848fe4f6b9154bffefdc230'
# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# User Loader
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    #user = users_db.get(user_id)
    return User.query.get(int(user_id))

from . import routes, auth
app.register_blueprint(auth.bp)
# Create all the tables in the database
with app.app_context():
    db.create_all()
