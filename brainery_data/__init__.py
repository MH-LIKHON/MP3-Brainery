"""
Flask Application Factory - Initializes and Configures the Application
"""

# =======================================================
# Module Imports - Core Dependencies & Libraries
# =======================================================

# Import necessary modules and dependencies
import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from bson.objectid import ObjectId
from brainery_data.models import User

# =======================================================
# Environment Setup & Global Instances
# =======================================================

# Load environment variables from .env file
load_dotenv()

# Initialize MongoDB, Flask-Login, and CSRF protection
mongo = PyMongo()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    """Create and configure the Flask application instance."""

    # =======================================================
    # Flask Application Initialization
    # =======================================================

    app = Flask(__name__,
                template_folder=os.path.join(
                    os.path.dirname(__file__), "templates"),
                static_folder=os.path.join(os.path.dirname(__file__), "static"))

    # =======================================================
    # Configure MongoDB Connection
    # =======================================================

    # Load MongoDB URI and secret key from environment variables
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY", "your_default_secret_key")

    # Ensure MongoDB URI is properly loaded
    if not app.config["MONGO_URI"]:
        raise ValueError("MONGO_URI is missing. Check your .env file.")

    # Initialize MongoDB connection
    try:
        mongo.init_app(app)
        mongo.db.users.find_one()  # Test MongoDB connection
        print("MongoDB connection is active!")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

    # =======================================================
    # Initialize Security Features
    # =======================================================

    # Enable CSRF protection for all form submissions
    csrf.init_app(app)

    # Initialize Flask-Login for handling user authentication
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # =======================================================
    # Flask-Login User Loader
    # =======================================================

    @login_manager.user_loader
    def load_user(user_id):
        """Retrieve user session from MongoDB by user ID."""
        try:
            user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user_data:
                return User(user_data)
            return None
        except Exception as e:
            print(f"Error loading user: {e}")
            return None

    # =======================================================
    # Register Flask Blueprints (Modular Routing)
    # =======================================================

    # Import route blueprints
    from brainery_data.routes.auth import auth
    from brainery_data.routes.dashboard import dashboard
    from brainery_data.routes.main import main
    from brainery_data.routes.register import register
    from brainery_data.routes.resource import resource

    # Register blueprints for different application modules
    # Handles user authentication
    app.register_blueprint(auth, url_prefix="/auth")
    # User dashboard routes
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(main)  # Main page routes
    # User registration routes
    app.register_blueprint(register, url_prefix="/register")
    # Resource management routes
    app.register_blueprint(resource, url_prefix="/resource")

    return app
