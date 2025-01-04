from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    
    # App configurations
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login if user not authenticated
    login_manager.login_message_category = 'info'  # Bootstrap alert category for messages

    # Register blueprints
    from brainery.routes.auth import auth  # Import the auth blueprint
    app.register_blueprint(auth)

    # Add more blueprints here in the future (e.g., main, dashboard, etc.)

    return app
