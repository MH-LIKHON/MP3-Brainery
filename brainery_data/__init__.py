import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect  # CSRF protection
from dotenv import load_dotenv  # Load environment variables
from bson.objectid import ObjectId  # Required for MongoDB user retrieval
from brainery_data.models import User  # Import the User model

# Load environment variables from .env file
load_dotenv()

# Initialize MongoDB, Flask-Login, and CSRF protection
mongo = PyMongo()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    """Application factory to create and configure the Flask app."""

    app = Flask(__name__,
                template_folder=os.path.join(
                    os.path.dirname(__file__), "templates"),
                static_folder=os.path.join(os.path.dirname(__file__), "static"))

    # Load MongoDB URI from environment
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY", "your_default_secret_key")

    # Ensure MONGO_URI is properly loaded
    if not app.config["MONGO_URI"]:
        raise ValueError("❌ MONGO_URI is missing. Check your .env file.")

    # Initialize MongoDB
    try:
        mongo.init_app(app)
        print("✅ Connected to MongoDB!")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")

    # Initialize CSRF protection
    csrf.init_app(app)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Flask-Login user loader function for MongoDB
    @login_manager.user_loader
    def load_user(user_id):
        """Load user from MongoDB"""
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
    from brainery_data.routes.register import register
    from brainery_data.routes.resource import resource

    # Register all blueprints
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(main)
    app.register_blueprint(register, url_prefix="/register")
    app.register_blueprint(resource, url_prefix="/resource")

    return app
