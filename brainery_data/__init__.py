from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Application factory to create and configure the Flask app."""
    # Load environment variables
    load_dotenv()

    # Create the Flask app
    app = Flask(
        __name__,
        static_folder='static',  # Explicitly specify the static folder
        template_folder='templates'  # Explicitly specify the template folder
    )

    # App configurations
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect unauthenticated users to login
    login_manager.login_message_category = 'info'  # Bootstrap alert class

    # Import the User model
    from brainery_data.models import User

    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Load user from the database by ID

    # Register blueprints
    from brainery_data.routes.auth import auth
    from brainery_data.routes.dashboard import dashboard
    from brainery_data.routes.main import main

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(main)

    return app
