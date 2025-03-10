from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from brainery_data import mongo
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv
import os

# ==============================================
# Load environment variables from .env
# ==============================================
load_dotenv()

# ==============================================
# Initialize Dashboard Blueprint
# ==============================================
dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# ==============================================
# Dashboard Home Route (Main Dashboard)
# ==============================================


@dashboard.route("/")
@login_required
def dashboard_main():
    """
    Render the main dashboard.
    Fetches user-specific resources from MongoDB.
    """
    print(f"🔍 Current User: {current_user} (ID: {current_user.id})")

    user_resources = list(mongo.db.resources.find(
        {"user_id": str(current_user.id)}
    ))

    return render_template("dashboard.html", resources=user_resources)

# ==============================================
# Retrieve Saved Study Topics (READ)
# ==============================================


@dashboard.route("/saved_topics", methods=["GET"])
@login_required
def get_saved_topics():
    """
    Fetch all saved topics for the logged-in user.
    """
    try:
        saved_topics = list(mongo.db.saved_topics.find(
            {"user_id": str(current_user.id)}
        ))

        for topic in saved_topics:
            topic["_id"] = str(topic["_id"])  # Convert ObjectId to string
            topic["timestamp"] = topic.get(
                "timestamp", "Unknown Date")  # Ensure timestamp exists

        print("✅ Saved Topics Retrieved Successfully!")
        return jsonify(saved_topics), 200
    except Exception as e:
        print(f"🚨 Error Fetching Saved Topics: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# ==============================================
# Get a Specific Topic (READ)
# ==============================================


@dashboard.route("/get_topic/<topic_id>", methods=["GET"])
@login_required
def get_topic(topic_id):
    """
    Retrieve a specific saved topic by its ID.
    """
    try:
        # Ensure valid ObjectId format
        if not ObjectId.is_valid(topic_id):
            return jsonify({"error": "Invalid Topic ID format"}), 400

        topic = mongo.db.saved_topics.find_one(
            {"_id": ObjectId(topic_id), "user_id": str(current_user.id)}
        )

        if topic:
            topic["_id"] = str(topic["_id"])  # Convert ObjectId to string
            topic["timestamp"] = topic.get("timestamp", "Unknown Date")
            return jsonify(topic), 200

        return jsonify({"error": "Topic not found"}), 404
    except Exception as e:
        print(f"🚨 Error Fetching Topic: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# ==============================================
# Save a Topic (CREATE)
# ==============================================


@dashboard.route("/save_topic", methods=["POST"])
@login_required
def save_topic():
    """
    Save a Wikipedia topic to the user's account.
    """
    try:
        data = request.get_json()
        print("🔍 Received Data from JS:", data)  # Debugging

        # Validate input
        if not data or "title" not in data:
            return jsonify({"error": "Invalid data - Title missing"}), 400

        topic_title = data["title"].strip()
        if not topic_title:
            return jsonify({"error": "Invalid data - Title is empty"}), 400

        # Save with correct timestamp
        timestamp = datetime.utcnow().isoformat()  # Store in ISO format

        mongo.db.saved_topics.insert_one({
            "user_id": str(current_user.id),
            "title": topic_title,
            "timestamp": timestamp  # Store correct timestamp
        })

        return jsonify({"message": "Topic saved successfully!", "timestamp": timestamp}), 201

    except Exception as e:
        print("🚨 Error saving topic:", str(e))
        return jsonify({"error": "Internal server error"}), 500

# ==============================================
# Update a Topic (UPDATE)
# ==============================================


@dashboard.route("/update_topic/<topic_id>", methods=["PUT"])
@login_required
def update_topic(topic_id):
    """
    Rename a saved topic for the user.
    """
    try:
        data = request.get_json()
        new_title = data.get("new_title")

        if not new_title:
            return jsonify({"error": "New title required"}), 400

        # Ensure valid ObjectId format
        if not ObjectId.is_valid(topic_id):
            return jsonify({"error": "Invalid Topic ID format"}), 400

        result = mongo.db.saved_topics.update_one(
            {"_id": ObjectId(topic_id), "user_id": str(current_user.id)},
            {"$set": {"title": new_title}}
        )

        if result.modified_count:
            return jsonify({"message": "Topic updated successfully!"}), 200

        return jsonify({"error": "Update failed"}), 400
    except Exception as e:
        print(f"🚨 Error Updating Topic: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# ==============================================
# Delete a Topic (DELETE)
# ==============================================


@dashboard.route("/delete_topic/<topic_id>", methods=["DELETE"])
@login_required
def delete_topic(topic_id):
    """
    Delete a saved topic.
    """
    try:
        # Ensure valid ObjectId format
        if not ObjectId.is_valid(topic_id):
            return jsonify({"error": "Invalid Topic ID format"}), 400

        result = mongo.db.saved_topics.delete_one(
            {"_id": ObjectId(topic_id), "user_id": str(current_user.id)}
        )

        if result.deleted_count:
            return jsonify({"message": "Topic deleted successfully!"}), 200

        return jsonify({"error": "Topic not found"}), 404
    except Exception as e:
        print(f"🚨 Error Deleting Topic: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
