from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from brainery_data.models import User
from brainery_data import mongo

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate user login."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user_data = mongo.db.users.find_one({"email": email})
        if user_data and check_password_hash(user_data["password"], password):
            user = User(user_data)
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            flash("Email already exists!", "danger")
        else:
            hashed_password = generate_password_hash(password)
            new_user = {"username": username, "email": email, "password": hashed_password}
            mongo.db.users.insert_one(new_user)
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
