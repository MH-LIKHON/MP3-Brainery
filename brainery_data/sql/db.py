# =======================================================
# SQLAlchemy Database Setup
# =======================================================

# Import required modules
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# =======================================================
# Load Environment Variables
# =======================================================

# Load environment variables from .env (for local development)
load_dotenv()

# =======================================================
# Database Configuration
# =======================================================

# Get database URL from environment or fall back to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///instance/brainery.db")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, future=True)

# =======================================================
# Session Factory
# =======================================================

# SessionLocal will be used in routes to interact with the database
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)