from app import app

if __name__ == '__main__':
    """
    Run the Flask application.

    This script starts the Flask application in debug mode.

    Usage:
    python run.py

    When this script is executed directly, the Flask application will run
    in debug mode. Debug mode is enabled for development, providing detailed 
    error pages and automatic reloading of the app on code changes.
    """
    app.run(debug=True)
