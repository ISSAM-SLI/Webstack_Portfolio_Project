from app import app

if __name__ == '__main__':
    """
    Entry point for running the Flask application.

    When this script is executed directly, the Flask application will run
    in debug mode. Debug mode is enabled for development, providing detailed 
    error pages and automatic reloading of the app on code changes.
    """
    app.run(debug=True)
