# =======================================================
# Authentication Routes
# =======================================================

# Import Flask utilities
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session

# Import Flask-Login helpers
from flask_login import login_user, logout_user, login_required, current_user

# Import password hashing utilities
from werkzeug.security import check_password_hash, generate_password_hash

# Import database session/model
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import UserSQL

# Import forms and session user adapter
from brainery_data.routes.form import LoginForm
from brainery_data.models import SessionUser

# Import SQL helpers
from sqlalchemy import func


# =======================================================
# Initialize Authentication Blueprint
# =======================================================

# Create blueprint for authentication routes
auth = Blueprint("auth", __name__)


# =======================================================
# User Login Route
# =======================================================

@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Authenticate against the database and start a Flask-Login session.
    """
    # Instantiate login form
    form = LoginForm()

    # Validate and process POST submissions
    if form.validate_on_submit():
        # Normalise inputs
        email = (form.email.data or "").strip().lower()
        password = (form.password.data or "").strip()

        # Open database session and look up user by case-insensitive email
        db = SessionLocal()
        try:
            sql_user = (
                db.query(UserSQL)
                  .filter(func.lower(UserSQL.email) == email)
                  .one_or_none()
            )
        finally:
            db.close()

        # Check credentials
        if not sql_user or not check_password_hash(sql_user.password or "", password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html", form=form)

        # Build session user from DB row and log them in
        user_obj = SessionUser(sql_user)
        login_user(user_obj, remember=True)

        # Role-based redirect
        if user_obj.role == "admin":
            flash("Logged in as Admin!", "success")
            return redirect(url_for("admin.admin_dashboard"))

        flash("Logged in successfully!", "success")
        return redirect(url_for("dashboard.dashboard_main"))

    # For GET or invalid form, render the login page
    return render_template("login.html", form=form)


# =======================================================
# User Logout Route
# =======================================================

@auth.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    """
    Log out the current user and clear session data.
    """
    # Terminate login session
    logout_user()

    # Clear any pending flash messages
    session.pop('_flashes', None)

    # JSON-aware response for AJAX vs normal navigation
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"message": "You have been logged out."}), 200

    # Redirect to login page
    return redirect(url_for("auth.login"))


# =======================================================
# Password Reset Route
# =======================================================

@auth.route("/reset_password", methods=["POST"])
def reset_password():
    """
    Reset user password. CSRF is enforced by the app-wide CSRF protection.
    Expects JSON: { "email": "...", "new_password": "..." }
    """
    # Ensure request is JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    # Parse body and normalise inputs
    try:
        data = request.get_json()
        email = (data.get("email") or "").strip().lower()
        new_password = (data.get("new_password") or "").strip()
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

    # Basic validation
    if not email or not new_password:
        return jsonify({"error": "Email and new password are required."}), 400
    if len(new_password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long."}), 400

    # Hash new password
    hashed = generate_password_hash(new_password)

    # Open database session
    db = SessionLocal()
    try:
        # Case-insensitive email lookup
        user = (
            db.query(UserSQL)
              .filter(func.lower(UserSQL.email) == email)
              .one_or_none()
        )

        # Fail if no matching user
        if not user:
            return jsonify({"error": "User not found."}), 404

        # Update password and commit
        user.password = hashed
        db.commit()

        # Success response
        return jsonify({"message": "Password reset successful."}), 200

    # Always close session
    finally:
        db.close()