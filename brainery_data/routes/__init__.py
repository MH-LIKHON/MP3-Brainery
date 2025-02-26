import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from dotenv import load_dotenv  # ✅ Load environment variables

# Load environment variables from .env file
load_dotenv()

# Initialize MongoDB and LoginManager
mongo = PyMongo()
login_manager = LoginManager()

def create_app():
    """Application factory to create and configure the Flask app."""
    
    app = Flask(__name__, 
                template_folder="brainery_data/templates", 
                static_folder="brainery_data/static")

    # App configurations
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/brainery")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your_default_secret_key")

    # Initialize MongoDB
    mongo.init_app(app)

    # Initialize Login Manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Redirect unauthenticated users to login
    login_manager.login_message_category = "info"  # Bootstrap alert class

    # Import the User model
    from brainery_data.models import User

    # Flask-Login user loader function for MongoDB
    @login_manager.user_loader
    def load_user(user_id):
        user_data = mongo.db.users.find_one({"_id": user_id})
        return User(user_data) if user_data else None  # Convert MongoDB user data to User object

    # Register Blueprints
    from brainery_data.routes.auth import auth
    from brainery_data.routes.dashboard import dashboard
    from brainery_data.routes.main import main
    from brainery_data.routes.resource import resource  # ✅ Ensure resource CRUD routes are registered

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(main)
    app.register_blueprint(resource, url_prefix="/resource")  # ✅ Adding resource CRUD routes

    return app
