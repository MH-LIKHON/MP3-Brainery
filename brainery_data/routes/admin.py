# =======================================================
# Admin Dashboard Route
# =======================================================

import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from brainery_data import mongo

# =======================================================
# Initialize Admin Blueprint
# =======================================================
admin = Blueprint('admin', __name__, url_prefix='/admin')

# =======================================================
# Admin Dashboard Route
# =======================================================


@admin.route('/')
@login_required
def admin_dashboard():
    """Render the admin dashboard with user management features."""

    # Check if the current user is an admin
    if not current_user.is_authenticated or current_user.role != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard.dashboard_main"))

    # Retrieve all users from the database
    users = list(mongo.db.users.find({}))

    # Count system statistics
    total_users = mongo.db.users.count_documents({})
    admin_users = mongo.db.users.count_documents({"role": "admin"})

    return render_template("admin.html", users=users, total_users=total_users, admin_users=admin_users)

# =======================================================
# Promote User to Admin
# =======================================================


@admin.route('/promote/<user_id>', methods=['POST'])
@login_required
def promote_user(user_id):
    """Promote a user to admin."""

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    try:
        user_object_id = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid User ID"}), 400

    # Ensure the user exists
    user = mongo.db.users.find_one({"_id": user_object_id})
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update the role
    result = mongo.db.users.update_one({"_id": user_object_id}, {
                                       "$set": {"role": "admin"}})

    if result.modified_count == 0:
        return jsonify({"error": "User is already an admin"}), 400

    return jsonify({"success": True}), 200

# =======================================================
# Delete User
# =======================================================


@admin.route('/delete/<user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete a user from the system."""

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    try:
        user_object_id = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid User ID"}), 400

    # Ensure the user exists before deleting
    user = mongo.db.users.find_one({"_id": user_object_id})
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Delete the user
    result = mongo.db.users.delete_one({"_id": user_object_id})

    if result.deleted_count == 0:
        return jsonify({"error": "Failed to delete user"}), 400

    return jsonify({"success": True}), 200
