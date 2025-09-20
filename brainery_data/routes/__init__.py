"""
Application Factory and Database Test Functions
"""

# =======================================================
# Module Imports - Core Dependencies & Libraries
# =======================================================

# Import necessary modules and dependencies
import os
from flask import Flask, jsonify
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Import session/user wrappers for SQL-backed auth
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import UserSQL
from brainery_data.models import SessionUser


# =======================================================
# Environment Setup and Initialization
# =======================================================

# Load environment variables from .env file
load_dotenv()

# Initialize Flask-Login and CSRF protection
login_manager = LoginManager()
csrf = CSRFProtect()


# =======================================================
# Application Factory
# =======================================================

def create_app():
    """Application factory to create and configure the Flask app."""

    # Create Flask application
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # =======================================================
    # Application Configurations
    # =======================================================

    # Set secret key from environment variables
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your_default_secret_key")

    # Configure Flask session storage
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    # =======================================================
    # Security and Authentication Features
    # =======================================================

    # Initialize CSRF protection and Flask-Login
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Flask-Login user loader function for SQL
    @login_manager.user_loader
    def load_user(user_id):
        """Reload user from SQL for Flask-Login sessions."""
        # Convert the string id to int for SQL PK
        try:
            uid = int(user_id)
        except (TypeError, ValueError):
            return None

        # Open a DB session and fetch the user
        db = SessionLocal()
        try:
            row = db.get(UserSQL, uid)
            if row:
                return SessionUser(row)
            return None
        finally:
            db.close()

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

    # Register blueprints with URL prefixes
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(main)

    # Keep register routes exactly as defined in register.py (uses '/register' inside file)
    app.register_blueprint(register, url_prefix="/register")

    app.register_blueprint(resource, url_prefix="/resource")
    app.register_blueprint(admin)

    return app


# =======================================================
# Database Test Function (SQL)
# =======================================================

def test_db():
    """Function to test the SQL database connection."""
    try:
        # Open a DB session
        db = SessionLocal()
        try:
            # Try to fetch a user row (or confirm empty table)
            row = db.query(UserSQL).first()
            if row:
                return jsonify({
                    "message": "Database connection successful!",
                    "sample_user": {"id": row.id, "email": row.email}
                }), 200
            else:
                return jsonify({"message": "Database connected, but no users found!"}), 200
        finally:
            # Always close the session
            db.close()
    except Exception as e:
        # Return error in JSON for quick visibility
        return jsonify({"error": str(e)}), 500