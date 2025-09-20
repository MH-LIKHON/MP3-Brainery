"""
Database Session User Adapter and Utility Models
"""

# =======================================================
# Import Required Modules
# =======================================================

# Import logging for diagnostics
import logging

# Import Flask-Login mixin for session identity
from flask_login import UserMixin

# Configure logging level for this module
logging.basicConfig(level=logging.ERROR)


# =======================================================
# SQL Session User Adapter
# =======================================================

class SessionUser(UserMixin):
    """
    Minimal user object for Flask-Login sessions, backed by SQL rows.
    Only includes fields the app actually uses.
    """

    def __init__(self, row):
        # Primary key is int in SQL; Flask-Login expects string
        self.id = str(getattr(row, "id", ""))

        # Basic identity fields
        self.username = getattr(row, "username", "") or ""
        self.first_name = getattr(row, "first_name", "") or ""
        self.last_name = getattr(row, "last_name", "") or ""

        # Normalised email (lowercased, trimmed)
        email = getattr(row, "email", "") or ""
        self.email = email.strip().lower()

        # Stored password hash (not used directly by Flask-Login)
        self.password = getattr(row, "password", "") or ""

        # Role string (defaults to "user")
        self.role = (getattr(row, "role", "") or "user").lower()

    # Check if the current session user has admin role
    def is_admin(self):
        return self.role == "admin"


# =======================================================
# Resource Model (Container Only)
# =======================================================

class Resource:
    """
    Lightweight resource container used by routes/templates.
    Persistence is handled in the SQL layer (see sql.models / routes).
    """

    def __init__(self, title, description, link, category, user_id):
        # Resource title
        self.title = title

        # Short description / summary
        self.description = description

        # External link to the resource
        self.link = link

        # Category/tag name
        self.category = category

        # Owning user id (string for template compatibility)
        self.user_id = str(user_id)