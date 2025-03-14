# =======================================================
# Authentication Routes
# =======================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from brainery_data.models import User
from brainery_data import mongo
from brainery_data.routes.form import LoginForm

# =======================================================
# Initialize Authentication Blueprint
# =======================================================

auth = Blueprint("auth", __name__)

# =======================================================
# User Login Route
# =======================================================


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Authenticate user credentials and handle login requests.
    """
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data.strip()

        try:
            # Retrieve user from MongoDB (case-insensitive)
            user_data = mongo.db.users.find_one(
                {"email": {"$regex": f"^{email}$", "$options": "i"}}
            )

            # Validate password and log the user in
            if user_data and check_password_hash(user_data["password"], password):
                user_obj = User(user_data)
                login_user(user_obj, remember=True)

                return redirect(url_for("dashboard.dashboard_main"))

            flash("❌ Invalid email or password.", "danger")

        except Exception as e:
            print(f"❌ Login Error: {e}")
            flash("⚠️ Login system error. Please try again later.", "danger")

    return render_template("login.html", form=form)

# =======================================================
# User Logout Route
# =======================================================


@auth.route("/logout")
@login_required
def logout():
    """
    Log out the current user and clear session data.
    """
    # Log the user out
    logout_user()

    # Flash a logout confirmation message
    flash("✅ You have been logged out.", "info")

    # Clear session data
    session.pop('_flashes', None)
    session.clear()

    # Debugging: output session status
    print("🔴 Session after clearing:", session)

    # Redirect user to the login page
    return redirect(url_for("auth.login"))

# =======================================================
# Password Reset Route
# =======================================================


@auth.route("/reset_password", methods=["POST"])
def reset_password():
    """
    Handle password reset requests securely.
    """
    # Log incoming request headers and data
    print(f"🔍 Incoming Request Headers: {request.headers}")
    print(f"🔍 Incoming Request Data: {request.get_data(as_text=True)}")

    # Verify request is JSON formatted
    if not request.is_json:
        print("❌ ERROR: Request is NOT JSON")
        return jsonify({"error": "Request must be JSON"}), 400

    try:
        # Parse email and new password from request JSON
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        new_password = data.get("new_password", "").strip()

    except Exception as e:
        print(f"❌ ERROR: JSON Parsing Failed - {e}")
        return jsonify({"error": "Invalid JSON format"}), 400

    # Validate required fields
    if not email or not new_password:
        print("❌ ERROR: Missing email or password")
        return jsonify({"error": "Email and new password are required."}), 400

    # Check new password strength
    if len(new_password) < 6:
        print("❌ ERROR: Password too short")
        return jsonify({"error": "Password must be at least 6 characters long."}), 400

    # Hash the new password securely
    hashed_password = generate_password_hash(new_password)

    # Update user password in MongoDB
    result = mongo.db.users.update_one(
        {"email": {"$regex": f"^{email}$", "$options": "i"}},
        {"$set": {"password": hashed_password}}
    )

    # Handle case where user is not found
    if result.matched_count == 0:
        print("❌ ERROR: User not found")
        return jsonify({"error": "User not found."}), 404

    # Confirm successful password reset
    print("✅ SUCCESS: Password reset successful")
    return jsonify({"message": "Password reset successful."}), 200
