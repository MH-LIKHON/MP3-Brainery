import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from brainery_data.models import User
from bson import ObjectId

# Load environment variables from .env file
load_dotenv()

# Initialize MongoDB, Flask-Login, and CSRF protection
mongo = PyMongo()
login_manager = LoginManager()
csrf = CSRFProtect()  # Create CSRFProtect object


def create_app():
    """Application factory to create and configure the Flask app."""

    app = Flask(__name__,
                template_folder="brainery_data/templates",
                static_folder="brainery_data/static")

    # App configurations
    app.config["MONGO_URI"] = os.getenv(
        "MONGO_URI", "mongodb://localhost:27017/brainery")
    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY", "your_default_secret_key")

    # ✅ Fix: Configure Flask session storage
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = "filesystem"

    # Initialize MongoDB, CSRF, and Flask-Login
    mongo.init_app(app)
    csrf.init_app(app)  # Initialize CSRF protection
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"  # Bootstrap alert class

    # Flask-Login user loader function for MongoDB
    @login_manager.user_loader
    def load_user(user_id):
        """User loader function for Flask-Login."""
        try:
            user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user_data:
                return User(user_data)
            return None
        except Exception as e:
            print(f"Error loading user: {e}")
            return None

    # Register Blueprints
    from brainery_data.routes.auth import auth
    from brainery_data.routes.dashboard import dashboard
    from brainery_data.routes.main import main
    # Register the register blueprint
    from brainery_data.routes.register import register
    # Register the resource blueprint
    from brainery_data.routes.resource import resource

    # Register all blueprints with their respective URL prefixes
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(main)  # Register main blueprint with no prefix
    # Register register blueprint with /register prefix
    app.register_blueprint(register, url_prefix="/register")
    # Register resource blueprint with /resource prefix
    app.register_blueprint(resource, url_prefix="/resource")

    return app
