from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from brainery_data.models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', category='success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid email or password.', category='danger')

    return render_template('login.html', title="Login")

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!', category='danger')
        elif User.query.filter_by(email=email).first():
            flash('Email is already registered!', category='danger')
        else:
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in.', category='success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', title="Register")

@auth.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('auth.login'))
