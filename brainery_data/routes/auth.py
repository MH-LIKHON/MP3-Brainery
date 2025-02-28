from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from brainery_data.models import User
from brainery_data import mongo

# Import LoginForm from register.py
from brainery_data.routes.register import LoginForm

# Initialize Blueprint for Authentication Routes
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate user login."""
    form = LoginForm()  # Initialize the login form

    if form.validate_on_submit():  # Check if the form is submitted and validated
        email = form.email.data
        password = form.password.data

        # Retrieve user from database using email
        # Ensure the method accepts mongo as an argument
        user = User.find_by_email(email, mongo)

        # Check if user exists and password is correct
        if user and check_password_hash(user.password, password):
            login_user(user)  # Log in the user
            flash("Login successful!", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
