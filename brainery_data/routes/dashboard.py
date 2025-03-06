from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from brainery_data import mongo
from bson.objectid import ObjectId

# ==============================================
# 🔹 INITIALIZE DASHBOARD BLUEPRINT
# ==============================================
dashboard = Blueprint("dashboard", __name__)

# ==============================================
# 🔹 DASHBOARD ROUTE
# ==============================================


@dashboard.route("/")
@login_required
def dashboard_home():
    """Render the user dashboard with user resources."""
    print(
        f"🔍 Checking user session in dashboard: {current_user.is_authenticated}")

    if not current_user.is_authenticated:
        print("❌ User session is NOT active. Redirecting to login.")

    user_resources = list(mongo.db.resources.find(
        {"user_id": current_user.id}))
    return render_template("dashboard.html", resources=user_resources)


# ==============================================
# 🔹 DASHBOARD UI (STUDY MATERIAL)
# ==============================================
@dashboard.route("/dashboard")
@login_required
def new_dashboard():
    """Render the new dashboard with study features."""
    saved_topics = list(mongo.db.saved_topics.find(
        {"user_id": current_user.id}))

    for topic in saved_topics:
        # Convert ObjectId to string for frontend use
        topic["_id"] = str(topic["_id"])

    return render_template("dashboard.html", saved_topics=saved_topics)


# ==============================================
# 🔹 SAVE A TOPIC (CREATE)
# ==============================================
@dashboard.route("/save_topic", methods=["POST"])
@login_required
def save_topic():
    """Save a Wikipedia topic to the user's account."""
    data = request.get_json()
    topic_title = data.get("title")

    if topic_title:
        mongo.db.saved_topics.insert_one(
            {"user_id": current_user.id, "title": topic_title})
        return jsonify({"message": "Topic saved successfully!"}), 201

    return jsonify({"error": "Invalid data"}), 400


# ==============================================
# 🔹 GET SAVED TOPICS (READ)
# ==============================================
@dashboard.route("/get_saved_topics", methods=["GET"])
@login_required
def get_saved_topics():
    """Retrieve the saved topics for the logged-in user."""
    saved_topics = list(mongo.db.saved_topics.find(
        {"user_id": current_user.id}))

    for topic in saved_topics:
        # Convert ObjectId to string for frontend use
        topic["_id"] = str(topic["_id"])

    return jsonify(saved_topics), 200


# ==============================================
# 🔹 UPDATE A TOPIC (RENAME / UPDATE)
# ==============================================
@dashboard.route("/update_topic/<topic_id>", methods=["PUT"])
@login_required
def update_topic(topic_id):
    """Rename a saved topic."""
    data = request.get_json()
    new_title = data.get("new_title")

    if new_title:
        result = mongo.db.saved_topics.update_one(
            {"_id": ObjectId(topic_id), "user_id": current_user.id},
            {"$set": {"title": new_title}}
        )

        if result.modified_count:
            return jsonify({"message": "Topic updated successfully!"}), 200

    return jsonify({"error": "Update failed"}), 400


# ==============================================
# 🔹 DELETE A TOPIC (DELETE)
# ==============================================
@dashboard.route("/delete_topic/<topic_id>", methods=["DELETE"])
@login_required
def delete_topic(topic_id):
    """Delete a saved topic."""
    result = mongo.db.saved_topics.delete_one(
        {"_id": ObjectId(topic_id), "user_id": current_user.id})

    if result.deleted_count:
        return jsonify({"message": "Topic deleted successfully!"}), 200

    return jsonify({"error": "Topic not found"}), 404
