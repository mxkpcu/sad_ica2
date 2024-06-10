from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app(config_class='config.Config'):
    """Create and configure instance of app"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions if not already initialized
    if not app.extensions.get('sqlalchemy'):
        db.init_app(app)
        mail.init_app(app)
    
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    
    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.events import events_bp
    from app.routes.profile import profile_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(main_bp)

    return app