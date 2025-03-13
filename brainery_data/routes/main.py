from flask import Blueprint, jsonify, render_template, current_app
from brainery_data import mongo

main = Blueprint('main', __name__)

# Home route


@main.route('/')
def index():
    """Home page route."""
    try:
        print("Rendering the home page")
        # Ensure the home page is rendered
        return render_template('index.html')
    except Exception as e:
        return jsonify({
            "error": f"Error rendering index.html: {str(e)}",
        }), 500

# Test MongoDB route


@main.route('/test_db')
def test_db():
    """Test if MongoDB connection is working."""
    try:
        user = mongo.db.users.find_one()  # Fetch one user from the database
        if user:
            # Convert ObjectId to string for JSON response
            user['_id'] = str(user['_id'])
            return jsonify(user)
        else:
            return jsonify({"error": "No users found in database"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching data from MongoDB: {str(e)}"}), 500
