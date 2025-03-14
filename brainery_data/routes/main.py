# =======================================================
# Main Blueprint - Routes for Homepage and Testing MongoDB
# =======================================================

from flask import Blueprint, jsonify, render_template, current_app
from brainery_data import mongo

# Initialize main blueprint
main = Blueprint('main', __name__)

# =======================================================
# Home Route
# =======================================================


@main.route('/')
def index():
    """Home page route."""
    try:
        print("Rendering the home page")
        # Render the home page template
        return render_template('index.html')
    except Exception as e:
        # Return JSON error response if rendering fails
        return jsonify({
            "error": f"Error rendering index.html: {str(e)}",
        }), 500

# =======================================================
# Test MongoDB Route
# =======================================================


@main.route('/test_db')
def test_db():
    """Test if MongoDB connection is working."""
    try:
        # Attempt to fetch one user from the MongoDB database
        user = mongo.db.users.find_one()
        if user:
            # Convert ObjectId to string for JSON response
            user['_id'] = str(user['_id'])
            # Return the user data as JSON
            return jsonify(user)
        else:
            # Return JSON error response if no users are found
            return jsonify({"error": "No users found in database"}), 404
    except Exception as e:
        # Return JSON error response if there’s an exception
        return jsonify({"error": f"An error occurred while fetching data from MongoDB: {str(e)}"}), 500
