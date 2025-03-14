# =======================================================
# User Routes
# =======================================================

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user, logout_user
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

# =======================================================
# Dashboard Home Route (Main Dashboard)
# =======================================================


@dashboard.route("/")
@login_required
def dashboard_main():
    """Render the main dashboard."""

    # Log current user information for debugging
    print(f"🔍 Current User: {current_user} (ID: {current_user.id})")

    # Render dashboard template
    return render_template("dashboard.html")

# =======================================================
# Retrieve All Subjects
# =======================================================


@dashboard.route("/subjects", methods=["GET"])
@login_required
def get_subjects():
    """Fetch all subjects from the database."""

    try:
        # Retrieve subjects from database
        subjects = list(mongo.db.subjects.find())

        # Convert ObjectId to string for JSON serialization
        for subject in subjects:
            subject["_id"] = str(subject["_id"])

        # Return subjects as JSON response
        return jsonify(subjects), 200

    except Exception as e:
        # Log error details for debugging
        print(f"🚨 Error Fetching Subjects: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# =======================================================
# Retrieve Topics by Subject ID
# =======================================================


@dashboard.route("/topics/<subject_id>", methods=["GET"])
@login_required
def get_topics(subject_id):
    """Fetch topics for a specific subject."""

    # Validate Subject ID format
    if not ObjectId.is_valid(subject_id):
        return jsonify({"error": "Invalid Subject ID"}), 400

    try:
        # Fetch topics from database matching subject ID
        topics = list(mongo.db.topics.find(
            {"subject_id": ObjectId(subject_id)}))

        # Convert ObjectIds to strings for JSON serialization
        for topic in topics:
            topic["_id"] = str(topic["_id"])
            topic["subject_id"] = str(topic["subject_id"])

        # Return topics as JSON response
        return jsonify(topics), 200

    except Exception as e:
        # Log error details for debugging
        print(f"🚨 Error Fetching Topics: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# =======================================================
# Retrieve a Specific Saved Topic
# =======================================================


@dashboard.route("/get_topic/<topic_id>", methods=["GET"])
@login_required
def get_topic(topic_id):
    """Retrieve details for a specific saved topic."""

    # Validate provided topic ID
    if not ObjectId.is_valid(topic_id):
        return jsonify({"error": "Invalid Topic ID format"}), 400

    try:
        # Retrieve topic from the database for the current user
        topic = mongo.db.saved_topics.find_one(
            {"_id": ObjectId(topic_id), "user_id": str(current_user.id)}
        )

        # Return topic details if found
        if topic:
            topic["_id"] = str(topic["_id"])
            topic["timestamp"] = topic.get("timestamp", "Unknown Date")
            return jsonify(topic), 200

        # Return error if topic not found
        return jsonify({"error": "Topic not found"}), 404

    except Exception as e:
        # Log error details for debugging
        print(f"🚨 Error Fetching Topic: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# =======================================================
# Save a New Topic
# =======================================================


@dashboard.route("/save_topic", methods=["POST"])
@login_required
def save_topic():
    """Save a topic to the user's account."""

    # Log received data from JavaScript
    try:
        data = request.get_json()
        print("🔍 Received Data from JS:", data)

        # Validate incoming request data
        if not data or "title" not in data:
            return jsonify({"error": "Invalid data - Title missing"}), 400

        # Retrieve and validate topic title
        topic_title = data["title"].strip()
        if not topic_title:
            return jsonify({"error": "Invalid data - Title missing"}), 400

        # Check if the topic already exists in user's saved topics
        existing_topic = mongo.db.saved_topics.find_one(
            {"user_id": str(current_user.id), "title": topic_title}
        )

        # Return error if topic already saved
        if existing_topic:
            return jsonify({"error": "Topic already saved!"}), 400

        # Retrieve topic description from database
        topic_data = mongo.db.topics.find_one({"title": topic_title})
        summary = topic_data["description"] if topic_data else "No summary available."

        # Generate timestamp for saved topic
        timestamp = datetime.utcnow().isoformat()

        # Insert new topic into user's saved topics collection
        mongo.db.saved_topics.insert_one({
            "title": topic_title,
            "summary": summary,
            "user_id": str(current_user.id),
            "timestamp": timestamp
        })

        # Return success response
        return jsonify({"message": "Topic saved successfully!", "timestamp": timestamp}), 201

    except Exception as e:
        # Log error details for debugging
        print("🚨 Error saving topic:", str(e))
        return jsonify({"error": "Internal server error"}), 500

# =======================================================
# Retrieve Saved Study Topics
# =======================================================


@dashboard.route("/saved_topics", methods=["GET"])
@login_required
def get_saved_topics():
    """Fetch saved study topics for the logged-in user."""

    try:
        # Retrieve user's saved topics from database
        saved_topics = list(mongo.db.saved_topics.find(
            {"user_id": str(current_user.id)}))

        # Convert ObjectIds and handle missing timestamps
        for topic in saved_topics:
            topic["_id"] = str(topic["_id"])
            topic["timestamp"] = topic.get("timestamp", "Unknown Date")

        # Log successful retrieval for debugging
        print("✅ Saved Topics Retrieved Successfully!")

        # Return saved topics as JSON
        return jsonify(saved_topics), 200

    except Exception as e:
        # Log error details for debugging
        print("🚨 Error Fetching Saved Topics:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

# =======================================================
# Update a Saved Topic
# =======================================================


@dashboard.route("/update_topic/<topic_id>", methods=["PUT"])
@login_required
def update_topic(topic_id):
    """Rename a saved topic for the user."""

    try:
        # Retrieve new title from request data
        data = request.get_json()
        new_title = data.get("new_title")

        # Validate new title presence
        if not new_title:
            return jsonify({"error": "New title required"}), 400

        # Validate topic ID format
        if not ObjectId.is_valid(topic_id):
            return jsonify({"error": "Invalid Topic ID format"}), 400

        # Check topic exists and belongs to the current user
        existing_topic = mongo.db.saved_topics.find_one(
            {"_id": ObjectId(topic_id), "user_id": str(current_user.id)}
        )

        # Return error if topic not found
        if not existing_topic:
            return jsonify({"error": "Topic not found"}), 404

        # Update topic title in database
        result = mongo.db.saved_topics.update_one(
            {"_id": ObjectId(topic_id), "user_id": str(current_user.id)},
            {"$set": {"title": new_title}}
        )

        # Return success message if update successful
        if result.modified_count:
            return jsonify({"message": "Topic updated successfully!"}), 200

        # Return error if no changes were made
        return jsonify({"error": "Update failed"}), 400

    except Exception as e:
        # Log error details for debugging
        print(f"🚨 Error Updating Topic: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# =======================================================
# Delete a Saved Topic (DELETE)
# =======================================================


@dashboard.route("/delete_topic/<topic_id>", methods=["DELETE"])
@login_required
def delete_topic(topic_id):
    """Delete a saved topic."""

    # Validate provided topic ID format
    if not ObjectId.is_valid(topic_id):
        return jsonify({"error": "Invalid Topic ID format"}), 400

    try:
        # Delete topic from the database
        result = mongo.db.saved_topics.delete_one(
            {"_id": ObjectId(topic_id), "user_id": str(current_user.id)}
        )

        # Return success response if deletion succeeded
        if result.deleted_count:
            return jsonify({"message": "Topic deleted successfully!"}), 200

        # Return error if topic not found
        return jsonify({"error": "Topic not found"}), 404

    except Exception as e:
        # Log error details for debugging
        print(f"🚨 Error Deleting Topic: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# =======================================================
# Logout User
# =======================================================


@dashboard.route("/auth/logout", methods=["POST"])
@login_required
def logout():
    """Log the user out and redirect to login."""

    try:
        # Log out the current user
        logout_user()

        # Log successful logout for debugging
        print("✅ User logged out successfully!")  # Debugging

        # Return success response
        return jsonify({"message": "Logout successful!"}), 200

    except Exception as e:
        # Log error details for debugging
        print(f"🚨 Logout Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
