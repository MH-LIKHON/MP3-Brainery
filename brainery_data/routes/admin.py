# =======================================================
# Admin Dashboard Routes
# =======================================================

# Import logging for diagnostics
import logging

# Import Flask utilities
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify

# Import login utilities
from flask_login import login_required, current_user

# Import SQL session and models
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import UserSQL


# =======================================================
# Initialize Admin Blueprint
# =======================================================

# Blueprint for admin routes
admin = Blueprint("admin", __name__, url_prefix="/admin")


# =======================================================
# Admin Dashboard Route
# =======================================================

@admin.route("/")
@login_required
def admin_dashboard():
    """Render the admin dashboard with user management features."""

    # Ensure the current user is an admin
    if not current_user.is_authenticated or current_user.role != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard.dashboard_main"))

    # Create SQL session
    db = SessionLocal()
    try:
        # Retrieve all users from the database
        users = db.query(UserSQL).all()

        # Count system statistics
        total_users = db.query(UserSQL).count()
        admin_users = db.query(UserSQL).filter(UserSQL.role == "admin").count()
    finally:
        # Always close the session
        db.close()

    # Render admin dashboard template
    return render_template("admin.html", users=users, total_users=total_users, admin_users=admin_users)


# =======================================================
# Promote User to Admin
# =======================================================

@admin.route("/promote/<int:user_id>", methods=["POST"])
@login_required
def promote_user(user_id):
    """Promote a user to admin."""

    # Ensure current user is admin
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    # Create SQL session
    db = SessionLocal()
    try:
        # Fetch target user by id
        user = db.get(UserSQL, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update user role if not already admin
        if user.role == "admin":
            return jsonify({"error": "User is already an admin"}), 400

        user.role = "admin"
        db.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        logging.error("Error promoting user: %s", e, exc_info=True)
        db.rollback()
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()


# =======================================================
# Delete User
# =======================================================

@admin.route("/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    """Delete a user from the system."""

    # Ensure current user is admin
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    # Create SQL session
    db = SessionLocal()
    try:
        # Fetch target user by id
        user = db.get(UserSQL, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Delete user
        db.delete(user)
        db.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        logging.error("Error deleting user: %s", e, exc_info=True)
        db.rollback()
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()