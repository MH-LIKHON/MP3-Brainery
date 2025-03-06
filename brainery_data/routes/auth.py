from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from brainery_data.models import User
from brainery_data import mongo
from brainery_data.routes.form import LoginForm  # Import the login form

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
            # Retrieve user from MongoDB (case-insensitive email search)
            user_data = mongo.db.users.find_one(
                {"email": {"$regex": f"^{email}$", "$options": "i"}}
            )

            if user_data and check_password_hash(user_data["password"], password):
                # Create a User object from database data
                user_obj = User(user_data)

                # Log in the user and set session
                login_user(user_obj, remember=True)

                flash("Login successful!", "success")

                # ✅ Fixed: Redirect to the correct dashboard
                return redirect(url_for("dashboard.dashboard_main"))
            else:
                # Display error message for incorrect credentials
                flash("Invalid email or password.", "danger")

        except Exception as e:
            print(f"❌ Login Error: {e}")
            flash("Login system error. Please try again later.", "danger")

    return render_template("login.html", form=form)


# ==============================================
# User Logout Route
# ==============================================

@auth.route("/logout")
@login_required
def logout():
    """
    Log out the current user and redirect to login page.
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


# ==============================================
# Password Reset Route
# ==============================================

@auth.route("/reset_password", methods=["POST"])
def reset_password():
    """
    Reset a user's password.
    - Expects JSON with 'email' and 'new_password'.
    - Hashes the new password before saving.
    - Updates the password in MongoDB.
    """
    data = request.get_json()
    email = data.get("email")
    new_password = data.get("new_password")

    if not email or not new_password:
        return jsonify({"error": "Email and new password are required."}), 400

    # Hash the new password before storing
    hashed_password = generate_password_hash(new_password)

    # Update the password in MongoDB
    result = mongo.db.users.update_one(
        {"email": {"$regex": f"^{email}$", "$options": "i"}},
        {"$set": {"password": hashed_password}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "User not found."}), 404

    return jsonify({"message": "Password reset successful."}), 200
