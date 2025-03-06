from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from brainery_data.models import User
from brainery_data import mongo
from brainery_data.routes.form import LoginForm  # ✅ Corrected Import Path

# Initialize Blueprint for Authentication Routes
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate user login."""
    print("🔍 Reached login function.")
    form = LoginForm()  # Initialize the login form

    if form.validate_on_submit():  # ✅ Validate only on form submission (POST)
        email = form.email.data.strip().lower()  # Ensure email is lowercase & trimmed
        password = form.password.data.strip()

        print(
            f"🔍 Attempting to log in user: {user_obj.username} (ID: {user_obj.id})")
        print(f"🔍 Login Attempt - Email: {email}")  # ✅ Debugging log

        try:
            # ✅ Retrieve user from MongoDB
            user_data = mongo.db.users.find_one({"email": email})

            if user_data and check_password_hash(user_data["password"], password):
                # Convert MongoDB user to User model
                user_obj = User(user_data)
                login_user(user_obj, remember=True)  # ✅ Keep user logged
                if current_user.is_authenticated:
                    print(
                        f"✅ User logged in successfully: {current_user.username} (ID: {current_user.id})")

                else:
                    print("❌ User login failed! Flask-Login session not active.")

                print(
                    f"✅ User logged in successfully: {user_obj.username} (ID: {user_obj.id})")

                print(
                    f"🔍 Flask-Login session active? {current_user.is_authenticated}")

                flash("✅ Login successful!", "success")
                return redirect(url_for("dashboard.dashboard_home"))
            else:
                flash("❌ Invalid email or password.", "danger")
                print("❌ Login failed - Incorrect credentials")

        except Exception as e:
            print(f"❌ Error fetching user from MongoDB: {str(e)}")
            flash("⚠️ Login system error. Please try again later.", "danger")

    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash("✅ You have been logged out.", "info")
    return redirect(url_for("auth.login"))
