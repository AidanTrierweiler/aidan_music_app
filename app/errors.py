from flask import render_template
from app import app, db

# Error handler for 404 Not Found errors
@app.errorhandler(404)
def not_found_error(error):
    # Render a custom 404 error page
    return render_template('404.html'), 404

# Error handler for 500 Internal Server errors
@app.errorhandler(500)
def internal_error(error):
    # Rollback the database session to prevent data corruption
    db.session.rollback()
    # Render a custom 500 error page
    return render_template('500.html'), 500
