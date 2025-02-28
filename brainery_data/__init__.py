import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect  # CSRF protection
from dotenv import load_dotenv  # Load environment variables
from brainery_data.models import User  # User model should be imported here

# Load environment variables from .env file
load_dotenv()

# Initialize MongoDB, Flask-Login, and CSRF protection
mongo = PyMongo()
login_manager = LoginManager()
csrf = CSRFProtect()  # Create CSRFProtect object

def create_app():
    """Application factory to create and configure the Flask app."""
    
    # Initialize Flask app
    app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), "templates"),
            static_folder=os.path.join(os.path.dirname(__file__), "static"))
    
    # App configurations
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/brainery")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your_default_secret_key")

    # Initialize MongoDB
    mongo.init_app(app)

    # Initialize CSRF protection
    csrf.init_app(app)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Redirect unauthenticated users to login
    login_manager.login_message_category = "info"  # Bootstrap alert class

    # Flask-Login user loader function for MongoDB
    @login_manager.user_loader
    def load_user(user_id):
        try:
            user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user_data:
                return User(user_data)
            return None
        except Exception as e:
            print(f"Error loading user: {e}")
            return None

    # Register Blueprints for routes
    from brainery_data.routes.auth import auth
    from brainery_data.routes.dashboard import dashboard
    from brainery_data.routes.main import main
    from brainery_data.routes.register import register  # Register the register blueprint
    from brainery_data.routes.resource import resource  # Register the resource blueprint

    # Register all blueprints with their respective URL prefixes
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(main)  # Register main blueprint with no prefix
    app.register_blueprint(register, url_prefix="/register")  # Register register blueprint with /register prefix
    app.register_blueprint(resource, url_prefix="/resource")  # Register resource blueprint with /resource prefix

    return app
