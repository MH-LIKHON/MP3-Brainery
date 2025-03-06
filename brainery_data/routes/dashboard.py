from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from brainery_data import mongo
from bson.objectid import ObjectId

# ==============================================
# Initialize Dashboard Blueprint
# ==============================================
dashboard = Blueprint("dashboard", __name__)

# ==============================================
# Dashboard Home Route (Main Dashboard)
# ==============================================


@dashboard.route("/dashboard")  # ✅ Fixed: This is the primary dashboard route
@login_required
def dashboard_main():
    """
    Render the main dashboard.
    - Fetches user-specific resources from MongoDB.
    """
    print(f"🔍 Current User: {current_user} (ID: {current_user.id})")

    user_resources = list(mongo.db.resources.find(
        {"user_id": str(current_user.id)}))

    return render_template("dashboard.html", resources=user_resources)

# ==============================================
# Retrieve Saved Study Topics
# ==============================================


@dashboard.route("/saved_topics")
@login_required
def saved_topics():
    """
    Render the dashboard with saved study topics.
    - Retrieves topics based on the logged-in user's ID.
    """
    saved_topics = list(mongo.db.saved_topics.find(
        {"user_id": str(current_user.id)}))

    for topic in saved_topics:
        # Convert ObjectId to string for frontend
        topic["_id"] = str(topic["_id"])

    return render_template("dashboard.html", saved_topics=saved_topics)

# ==============================================
# Save a Topic (Create)
# ==============================================


@dashboard.route("/save_topic", methods=["POST"])
@login_required
def save_topic():
    """
    Save a Wikipedia topic to the user's account.
    - Accepts JSON input containing the topic title.
    - Stores the topic in MongoDB.
    """
    data = request.get_json()
    topic_title = data.get("title")

    if not topic_title:
        return jsonify({"error": "Invalid data"}), 400

    mongo.db.saved_topics.insert_one(
        {"user_id": str(current_user.id), "title": topic_title})

    return jsonify({"message": "Topic saved successfully!"}), 201

# ==============================================
# Get Saved Topics (Read)
# ==============================================


@dashboard.route("/get_saved_topics", methods=["GET"])
@login_required
def get_saved_topics():
    """
    Retrieve the saved topics for the logged-in user.
    - Fetches all topics belonging to the user from MongoDB.
    """
    saved_topics = list(mongo.db.saved_topics.find(
        {"user_id": str(current_user.id)}))

    for topic in saved_topics:
        topic["_id"] = str(topic["_id"])  # Convert ObjectId to string

    return jsonify(saved_topics), 200

# ==============================================
# Update a Topic (Rename/Update)
# ==============================================


@dashboard.route("/update_topic/<topic_id>", methods=["PUT"])
@login_required
def update_topic(topic_id):
    """
    Rename a saved topic for the user.
    - Accepts JSON input with the new topic title.
    - Updates the corresponding record in MongoDB.
    """
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

# ==============================================
# Delete a Topic (Delete)
# ==============================================


@dashboard.route("/delete_topic/<topic_id>", methods=["DELETE"])
@login_required
def delete_topic(topic_id):
    """
    Delete a saved topic.
    - Deletes the topic from MongoDB if it exists.
    """
    result = mongo.db.saved_topics.delete_one(
        {"_id": ObjectId(topic_id), "user_id": str(current_user.id)}
    )

    if result.deleted_count:
        return jsonify({"message": "Topic deleted successfully!"}), 200

    return jsonify({"error": "Topic not found"}), 404
