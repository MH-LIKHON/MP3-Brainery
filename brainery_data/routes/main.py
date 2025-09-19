# =======================================================
# Main Blueprint - Routes for Homepage and Database Test
# =======================================================

# Import Flask primitives
from flask import Blueprint, jsonify, render_template

# Import database session and model
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import UserSQL


# =======================================================
# Initialize Main Blueprint
# =======================================================

# Blueprint for main routes
main = Blueprint("main", __name__)


# =======================================================
# Home Route
# =======================================================

@main.route("/")
def index():
    """Render the home page."""

    try:
        # Diagnostic message to server console
        print("Rendering the home page")

        # Render homepage template
        return render_template("index.html")

    except Exception as e:
        # Return JSON error response if rendering fails
        return jsonify({
            "error": f"Error rendering index.html: {str(e)}",
        }), 500


# =======================================================
# Test Database Route
# =======================================================

@main.route("/test_db")
def test_db():
    """Test if the SQL database connection is working."""

    try:
        # Open a new SQLAlchemy session
        db = SessionLocal()
        try:
            # Fetch the first user row from the database
            user = db.query(UserSQL).first()
        finally:
            # Always close the session
            db.close()

        # If a user exists, return their data as JSON
        if user:
            return jsonify({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }), 200
        else:
            # No users found in the database
            return jsonify({"error": "No users found in database"}), 404

    except Exception as e:
        # Return JSON error response if query fails
        return jsonify({
            "error": f"An error occurred while fetching data from the database: {str(e)}",
        }), 500