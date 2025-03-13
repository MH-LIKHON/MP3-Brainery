from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from brainery_data.models import User
from brainery_data import mongo
from brainery_data.routes.form import LoginForm


# ==============================================
# Initialize Authentication Blueprint
# ==============================================
auth = Blueprint("auth", __name__)

# ==============================================
# User Login Route (Handles GET and POST requests)
# ==============================================


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Authenticate user login.
    - Validates form data.
    - Checks user credentials in the database.
    - Logs in the user if credentials are valid.
    - Redirects to the dashboard upon success.
    """
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data.strip()

        try:
            # ✅ Retrieve user from MongoDB (case-insensitive search)
            user_data = mongo.db.users.find_one(
                {"email": {"$regex": f"^{email}$", "$options": "i"}}
            )

            # ✅ Validate password and log in user
            if user_data and check_password_hash(user_data["password"], password):
                user_obj = User(user_data)
                login_user(user_obj, remember=True)

                return redirect(url_for("dashboard.dashboard_main"))

            flash("❌ Invalid email or password.", "danger")

        except Exception as e:
            print(f"❌ Login Error: {e}")
            flash("⚠️ Login system error. Please try again later.", "danger")

    return render_template("login.html", form=form)

# ==============================================
# User Logout Route
# ==============================================


@auth.route("/logout")
@login_required
def logout():
    """
    Log out the current user and redirect to the home page.
    """
    # Log the user out
    logout_user()  # Log the user out

    # Flash the logout message
    flash("✅ You have been logged out.", "info")

    # Manually clear the session and flash messages
    session.pop('_flashes', None)  # Manually remove flash messages
    session.clear()  # Clear all session data

    # Debugging session status
    # Debug: Show session after clearing
    print("🔴 Session after clearing:", session)

    # Redirect to the home page (index)
    return redirect(url_for("auth.login"))


# ==============================================
# Password Reset Route
# ==============================================


@auth.route("/reset_password", methods=["POST"])
def reset_password():
    """
    Reset a user's password.
    - Logs incoming request headers and data for debugging.
    - Ensures request contains valid JSON.
    - Updates the password securely in MongoDB.
    """

    # ✅ Log the Request Headers & Data
    print(f"🔍 Incoming Request Headers: {request.headers}")
    # Log raw data
    print(f"🔍 Incoming Request Data: {request.get_data(as_text=True)}")

    # ✅ Check if the request is JSON
    if not request.is_json:
        print("❌ ERROR: Request is NOT JSON")
        return jsonify({"error": "Request must be JSON"}), 400

    try:
        # ✅ Parse JSON Data
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        new_password = data.get("new_password", "").strip()

    except Exception as e:
        print(f"❌ ERROR: JSON Parsing Failed - {e}")
        return jsonify({"error": "Invalid JSON format"}), 400

    # ✅ Validate Fields
    if not email or not new_password:
        print("❌ ERROR: Missing email or password")
        return jsonify({"error": "Email and new password are required."}), 400

    # ✅ Password Strength Check
    if len(new_password) < 6:
        print("❌ ERROR: Password too short")
        return jsonify({"error": "Password must be at least 6 characters long."}), 400

    # ✅ Hash Password
    hashed_password = generate_password_hash(new_password)

    # ✅ Update MongoDB
    result = mongo.db.users.update_one(
        {"email": {"$regex": f"^{email}$", "$options": "i"}},
        {"$set": {"password": hashed_password}}
    )

    if result.matched_count == 0:
        print("❌ ERROR: User not found")
        return jsonify({"error": "User not found."}), 404

    print("✅ SUCCESS: Password reset successful")
    return jsonify({"message": "Password reset successful."}), 200
