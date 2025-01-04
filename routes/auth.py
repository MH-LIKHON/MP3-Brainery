from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from brainery.models import User, db

auth = Blueprint('auth', __name__)

# ==============================
# Route: Login
# ==============================
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', category='success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password. Please try again.', category='error')

    return render_template('login.html', title="Login")

# ==============================
# Route: Register
# ==============================
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation checks
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', category='error')
        elif User.query.filter_by(email=email).first():
            flash('Email is already registered. Please log in.', category='error')
        else:
            # Create a new user
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in.', category='success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', title="Register")

# ==============================
# Route: Logout
# ==============================
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))
