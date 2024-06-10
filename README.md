# SAD-ICA2 Project

## Overview
Private Event Portal is a web application built with Flask. It features user authentication, event management, and profile management. The application uses SQLAlchemy for database interactions and Flask-Mail for email notifications.

## Features
- User Registration and Login
- Event Creation, Editing, and Deletion
- User Profile Management
- CAPTCHA Verification for security

## Installation

### Prerequisites
- Python 3.12
- Flask
- SQLAlchemy
- Flask-Mail

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/mxkpcu/sad_ica2.git
    cd sad_ica2
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. (optional) Set up the environment variables for email configurations (in `.env` file):
    ```env
    MAIL_SERVER=smtp.yourmailserver.com
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME=your-email@example.com
    MAIL_PASSWORD=your-password
    ```

5. Initialize the database and make migration:
    ```bash
    export FLASK_APP=manage.py
    python -m flask db init
    python -m flask db migrate -m "Initial migration."
    python -m flask db upgrade
    ```

6. Run the application:
    ```bash
    python -m flask run
    ```

## Running Tests
To run the tests and check the test coverage, use:
```bash
pytest --cov=app tests/
```
