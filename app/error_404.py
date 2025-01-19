from flask import render_template
from app import app  # Import the app instance

@app.errorhandler(404)
def page_not_found(e):
    """
    Custom 404 error handler that displays a user-friendly message when a page is not found.
    """
    return render_template('404.html'), 404
