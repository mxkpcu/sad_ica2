from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_session import Session
from sqlalchemy import inspect, MetaData, Table, Column, Integer, String, LargeBinary, DateTime

db = SQLAlchemy()
mail = Mail()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    mail.init_app(app)
    
    # Configure session
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    
    Session(app)
    
    from app.routes.auth import auth_bp
    from app.routes.events import events_bp
    from app.routes.profile import profile_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
