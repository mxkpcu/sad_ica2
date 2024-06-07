from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import User
from werkzeug.security import generate_password_hash
from app.routes.auth import validate_email

# Define the Blueprint for profile routes
profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
def profile():
    """
    Route to display the user's profile.
    """
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('profile.html', user=user, active_page='profile')
    return redirect(url_for('auth.login'))

@profile_bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """
    Route to edit the user's profile. Handles both GET and POST requests.
    """
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)

        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            phone = request.form.get('phone', '')

            # Validate email
            if not validate_email(email):
                flash('Invalid email address')
                return redirect(url_for('profile.edit_profile'))

            # Update user's password if provided
            if password:
                user.password = generate_password_hash(password)
            
            # Update user's profile information
            user.username = username
            user.email = email
            user.phone = phone
            db.session.commit()

            return redirect(url_for('profile.profile'))

        return render_template('edit_profile.html', user=user, active_page='profile')
    return redirect(url_for('auth.login'))

@profile_bp.route('/delete_profile', methods=['GET', 'POST'])
def delete_profile():
    """
    Route to delete the user's profile. Handles both GET and POST requests.
    """
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)

        if request.method == 'POST':
            db.session.delete(user)
            db.session.commit()
            session.pop('user_id', None)
            return redirect(url_for('main.home'))

        return render_template('delete_profile.html', active_page='profile')
    return redirect(url_for('auth.login'))
