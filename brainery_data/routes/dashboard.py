from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from brainery_data import mongo
from bson.objectid import ObjectId
from datetime import datetime
import os

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
    """
    print(f"🔍 Current User: {current_user} (ID: {current_user.id})")
    return render_template("dashboard.html")

# ==============================================
# Retrieve All Subjects (READ)
# ==============================================


@dashboard.route("/subjects", methods=["GET"])
@login_required
def get_subjects():
    """
    Fetch all subjects from the database.
    """
    try:
        subjects = list(mongo.db.subjects.find())

        for subject in subjects:
            subject["_id"] = str(subject["_id"])  # Convert ObjectId to string

        return jsonify(subjects), 200
    except Exception as e:
        print(f"🚨 Error Fetching Subjects: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# ==============================================
# Retrieve Topics for a Subject (READ)
# ==============================================


@dashboard.route("/topics/<subject_id>", methods=["GET"])
@login_required
def get_topics(subject_id):
    """
    Fetch all topics belonging to a specific subject.
    """
    try:
        topics = list(mongo.db.topics.find(
            {"subject_id": ObjectId(subject_id)}))

        for topic in topics:
            topic["_id"] = str(topic["_id"])  # Convert ObjectId to string
            # Convert ObjectId to string
            topic["subject_id"] = str(topic["subject_id"])

        return jsonify(topics), 200
    except Exception as e:
        print(f"🚨 Error Fetching Topics: {e}")
        return jsonify({"error": "Invalid Subject ID"}), 400

# ==============================================
# Retrieve a Single Topic (READ)
# ==============================================


@dashboard.route("/get_topic/<topic_id>", methods=["GET"])
@login_required
def get_topic(topic_id):
    """
    Retrieve a specific saved topic by its ID.
    """
    try:
        topic = mongo.db.saved_topics.find_one(
            {"_id": ObjectId(topic_id), "user_id": str(current_user.id)}
        )

        if topic:
            topic["_id"] = str(topic["_id"])  # Convert ObjectId to string
            return jsonify(topic), 200

        return jsonify({"error": "Topic not found"}), 404
    except Exception as e:
        print(f"🚨 Error Fetching Topic: {e}")
        return jsonify({"error": "Invalid Topic ID"}), 400

# ==============================================
# Save a Topic (CREATE)
# ==============================================


@dashboard.route("/save_topic", methods=["POST"])
@login_required
def save_topic():
    """
    Save a topic to the user's saved topics list.
    """
    try:
        data = request.get_json()
        print("🔍 Received Data from JS:", data)

        if not data or "title" not in data:
            return jsonify({"error": "Invalid data - Title missing"}), 400

        topic_title = data["title"].strip()
        if not topic_title:
            return jsonify({"error": "Invalid data - Title is empty"}), 400

        # Save topic with correct timestamp
        timestamp = datetime.utcnow().isoformat()

        mongo.db.saved_topics.insert_one({
            "user_id": str(current_user.id),
            "title": topic_title,
            "timestamp": timestamp
        })

        return jsonify({"message": "Topic saved successfully!", "timestamp": timestamp}), 201

    except Exception as e:
        print("🚨 Error saving topic:", str(e))
        return jsonify({"error": "Internal server error"}), 500

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

        print("✅ Saved Topics Retrieved Successfully!")
        return jsonify(saved_topics), 200
    except Exception as e:
        print(f"🚨 Error Fetching Saved Topics: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

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
        result = mongo.db.saved_topics.delete_one(
            {"_id": ObjectId(topic_id), "user_id": str(current_user.id)}
        )

        if result.deleted_count:
            return jsonify({"message": "Topic deleted successfully!"}), 200

        return jsonify({"error": "Topic not found"}), 404
    except Exception as e:
        print(f"🚨 Error Deleting Topic: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
