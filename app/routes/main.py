from flask import Blueprint, render_template, session
from app.models import User

# Define the Blueprint for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Route for the home page. Displays a welcome message with the user's information if logged in.
    """
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('index.html', user=user, active_page='home')
    return render_template('index.html', user=None, active_page='home')
