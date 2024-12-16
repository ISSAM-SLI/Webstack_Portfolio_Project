from flask import Flask
from flask_login import LoginManager
from app.models import users_db
 

app = Flask(__name__)
app.secret_key = 'd28ebc859848fe4f6b9154bffefdc230'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    print(f"Attempting to load user with ID: {user_id}")
    user = users_db.get(user_id)
    print(f"Loaded user: {user}")
    return user

from . import routes, auth
# Import routes for authentication and regular app functionality
app.register_blueprint(auth.bp)
