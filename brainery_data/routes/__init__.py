"""
Application Factory and Database Test Functions
"""

# =======================================================
# Module Imports - Core Dependencies & Libraries
# =======================================================

# Import necessary modules and dependencies
import os
from flask import Flask, jsonify, Blueprint
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Middleware for reverse proxy headers
from werkzeug.middleware.proxy_fix import ProxyFix

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
    # Prefix-Aware Deployment (Environment-Driven)
    # =======================================================
    # If MP3_PREFIX is set (e.g., "/mp3-brainery" on hosting),
    # adjust Flask root path and cookie path accordingly.
    _prefix = os.getenv("MP3_PREFIX", "").strip()
    if _prefix:
        app.config["APPLICATION_ROOT"] = _prefix
        app.config["SESSION_COOKIE_PATH"] = _prefix

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
    # Proxy & Middleware Configuration
    # =======================================================
    # Trust headers from reverse proxy (Nginx) including X-Forwarded-Prefix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Ensure SCRIPT_NAME is set when proxied behind a prefix
    app.wsgi_app = _PrefixFromHeaderMiddleware(app.wsgi_app)

    # =======================================================
    # Proxy & Middleware Configuration
    # =======================================================
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.wsgi_app = _PrefixFromHeaderMiddleware(app.wsgi_app)

    # =======================================================
    # Register Application Blueprints
    # (Prefix handled via SCRIPT_NAME from middleware)
    # =======================================================

    # Import blueprints
    from brainery_data.routes.auth import auth
    from brainery_data.routes.dashboard import dashboard
    from brainery_data.routes.main import main
    from brainery_data.routes.register import register
    from brainery_data.routes.resource import resource
    from brainery_data.routes.admin import admin

    # Register blueprints (no root wrapper)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(main)
    app.register_blueprint(register, url_prefix="/register")
    app.register_blueprint(resource, url_prefix="/resource")
    app.register_blueprint(admin, url_prefix="/admin")

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
    
# =======================================================
# Prefix Middleware Class
# =======================================================
# This middleware reads X-Forwarded-Prefix or X-Script-Name
# from Nginx and adjusts SCRIPT_NAME and PATH_INFO accordingly.
# It is a no-op on local dev (no header set).
class _PrefixFromHeaderMiddleware:
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        prefix = environ.get("HTTP_X_FORWARDED_PREFIX") or environ.get("HTTP_X_SCRIPT_NAME")
        if prefix:
            environ["SCRIPT_NAME"] = prefix
            path_info = environ.get("PATH_INFO", "")
            if path_info.startswith(prefix):
                environ["PATH_INFO"] = path_info[len(prefix):] or "/"
        return self.app(environ, start_response)