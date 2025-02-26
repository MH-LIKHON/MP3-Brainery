import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv  # ✅ Ensure this is imported

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, 
                template_folder="brainery_data/templates", 
                static_folder="brainery_data/static")

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')  # Example DB
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_default_secret_key')  # Secret Key

    db.init_app(app)
    login_manager.init_app(app)

    from brainery_data.routes.main import main
    app.register_blueprint(main)

    return app
