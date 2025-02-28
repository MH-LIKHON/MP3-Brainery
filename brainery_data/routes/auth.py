from flask import Blueprint, render_template, request, redirect, url_for, flash
from brainery_data.routes.register import RegisterForm
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from brainery_data.models import User
from brainery_data import mongo

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate user login."""
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.find_by_email(email, mongo)  # Pass mongo to the method

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
