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
    """Authenticate user credentials and handle login requests."""
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data.strip()

        try:
            # Retrieve user from MongoDB
            user_data = mongo.db.users.find_one(
                {"email": {"$regex": f"^{email}$", "$options": "i"}}
            )

            # Debugging: Print retrieved user data
            print(f"Retrieved User Data: {user_data}")

            # Ensure correct credentials
            if not user_data or not check_password_hash(user_data.get("password", ""), password):
                flash("Invalid email or password.", "danger")
                return render_template("login.html", form=form)

            # User authentication successful
            user_obj = User(user_data)
            login_user(user_obj, remember=True)

            # Redirect based on user role
            if user_obj.is_admin():
                flash("Logged in as Admin!", "success")
                return redirect(url_for("admin.admin_dashboard"))
            else:
                flash("Logged in successfully!", "success")
                return redirect(url_for("dashboard.dashboard_main"))

        except Exception as e:
            print(f"Unexpected Login Error: {e}")
            return render_template("login.html", form=form)

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
    # Log the user out
    logout_user()

    # Clear session data
    session.pop('_flashes', None) 

    # Debugging: output session status
    print("🔴 Session after clearing:", session)

    # Check if the request is AJAX (JavaScript fetch or $.ajax)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"message": "You have been logged out."}), 200

    # Redirect to login page for normal requests (non-AJAX)
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
