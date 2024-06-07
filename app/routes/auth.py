from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db, mail
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message
import random
import re
import dns.resolver

# Define the Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Create a URL safe serializer instance for token generation
s = URLSafeTimedSerializer('your_secret_key')

def send_confirmation_email(email, token):
    """
    Function to send confirmation email with a token.
    """
    msg = Message('Email Confirmation', sender='no-reply@example.com', recipients=[email])
    msg.body = f'Please confirm your registration by clicking the following link: http://127.0.0.1:5000/confirm_email/{token}'
    try:
        mail.send(msg)
    except:
        pass

def validate_email(email):
    """
    Function to validate email format and check MX records.
    """
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(regex, email):
        try:
            domain = email.split('@')[1]
            records = dns.resolver.resolve(domain, 'MX')
            return True
        except:
            return False
    return False

def generate_captcha():
    """
    Function to generate a simple math CAPTCHA.
    """
    operators = ['+', '-']
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(operators)
    captcha = f"{num1} {operator} {num2}"
    answer = eval(captcha)
    session['captcha_answer'] = answer
    return captcha

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login. Handles both GET and POST requests.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        captcha = request.form['captcha']

        # Check CAPTCHA
        if 'captcha_answer' not in session or int(captcha) != session['captcha_answer']:
            flash('Incorrect CAPTCHA, please try again.')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()
        
        # Authenticate user
        if user and check_password_hash(user.password, password):
            if user.email_confirmed:
                session['user_id'] = user.id
                return redirect(url_for('profile.profile'))
            else:
                flash('Please confirm your email before logging in.')
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('auth.login'))

    captcha = generate_captcha()
    return render_template('login.html', captcha=captcha)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route for user registration. Handles both GET and POST requests.
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        phone = request.form.get('phone', '')
        captcha = request.form['captcha']

        # Check CAPTCHA
        if 'captcha_answer' not in session or int(captcha) != session['captcha_answer']:
            flash('Incorrect CAPTCHA, please try again.')
            return redirect(url_for('auth.register'))

        # Validate email
        if not validate_email(email):
            flash('Invalid email address')
            return redirect(url_for('auth.register'))

        # Check if user or email already exists
        if User.query.filter((User.email == email) | (User.username == username)).first():
            flash('Username or email already exists')
            return redirect(url_for('auth.register'))

        # Create new user
        user = User(username=username, email=email, password=password, phone=phone)
        db.session.add(user)
        db.session.commit()

        # Send confirmation email
        token = s.dumps(email, salt='email-confirm')
        send_confirmation_email(email, token)

        return render_template('message.html', message='A confirmation email has been sent to your email address.', token=token)

    captcha = generate_captcha()
    return render_template('register.html', captcha=captcha)

@auth_bp.route('/confirm_email/<token>')
def confirm_email(token):
    """
    Route to confirm user's email with a token.
    """
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return render_template('message.html', message='The confirmation link has expired.')

    user = User.query.filter_by(email=email).first()
    user.email_confirmed = True
    db.session.commit()

    return render_template('message.html', message='Your email has been confirmed! You can now log in.')

@auth_bp.route('/logout')
def logout():
    """
    Route to log out the user.
    """
    session.pop('user_id', None)
    return redirect(url_for('main.home'))
