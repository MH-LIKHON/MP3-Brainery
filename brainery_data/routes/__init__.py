"""
Application Factory and Database Test Functions
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
from brainery_data.models import User
from bson import ObjectId

# =======================================================
# Environment Setup and Initialization
# =======================================================

# Load environment variables from .env file
load_dotenv()

# Initialize MongoDB, Flask-Login, and CSRF protection
mongo = PyMongo()
login_manager = LoginManager()
csrf = CSRFProtect()

# =======================================================
# Application Factory
# =======================================================


def create_app():
    """Application factory to create and configure the Flask app."""

    # Create Flask application
    app = Flask(__name__,
                template_folder="brainery_data/templates",
                static_folder="brainery_data/static")

    # =======================================================
    # Application Configurations
    # =======================================================

    # Set MongoDB URI and secret key from environment variables
    app.config["MONGO_URI"] = os.getenv(
        "MONGO_URI", "mongodb://localhost:27017/brainery")
    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY", "your_default_secret_key")

    # Configure Flask session storage
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = "filesystem"

    # =======================================================
    # Security and Authentication Features
    # =======================================================

    # Initialize MongoDB, CSRF protection, and Flask-Login
    mongo.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Flask-Login user loader function for MongoDB
    @login_manager.user_loader
    def load_user(user_id):
        """User loader function for Flask-Login."""
        try:
            # Fetch user data from MongoDB using ObjectId
            user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user_data:
                return User(user_data)
            return None
        except Exception as e:
            print(f"Error loading user: {e}")
            return None

    # =======================================================
    # Register Application Blueprints
    # =======================================================

    # Import blueprints
    from brainery_data.routes.auth import auth
    from brainery_data.routes.dashboard import dashboard
    from brainery_data.routes.main import main
    from brainery_data.routes.register import register
    from brainery_data.routes.resource import resource
    from brainery_data.routes.admin import admin

    # Register blueprints with corresponding URL prefixes
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(main)
    app.register_blueprint(register, url_prefix="/register")
    app.register_blueprint(resource, url_prefix="/resource")
    app.register_blueprint(admin)

    return app

# =======================================================
# Database Test Function
# =======================================================


def test_db():
    """Function to test the MongoDB connection."""
    try:
        # Attempt to fetch a document from MongoDB
        test_data = mongo.db.saved_topics.find_one()
        if test_data:
            return jsonify({"message": "Database connection successful!", "sample_data": str(test_data)}), 200
        else:
            return jsonify({"message": "Database connected, but no data found!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
