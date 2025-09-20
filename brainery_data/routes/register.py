# =======================================================
# User Registration Routes
# =======================================================

# Import logging for diagnostics
import logging

# Import Flask utilities
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify

# Import password hashing
from werkzeug.security import generate_password_hash

# Import WTForms base and fields
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

# Import datetime for timestamps
from datetime import datetime

# Import app-level CSRF and SQL session/model
from brainery_data.routes import csrf
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import UserSQL

# Import SQLAlchemy exceptions
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# SQL helper for case-insensitive lookup
from sqlalchemy import func


# =======================================================
# Logging Setup
# =======================================================

# Configure base logging level
logging.basicConfig(level=logging.INFO)


# =======================================================
# Initialize Registration Blueprint
# =======================================================

# Create blueprint for registration routes
register = Blueprint('register', __name__)


# =======================================================
# Registration Form Class
# =======================================================

# Define the user registration form fields and validators
class RegisterForm(FlaskForm):
    # User's first name
    first_name = StringField('First Name', validators=[DataRequired()])

    # User's last name
    last_name = StringField('Last Name', validators=[DataRequired()])

    # User's date of birth (expects YYYY-MM-DD from <input type="date">)
    dob = DateField('Date of Birth', validators=[DataRequired()])

    # User's email address
    email = StringField('Email Address', validators=[DataRequired(), Email()])

    # User's phone number
    phone = StringField('Phone Number', validators=[DataRequired()])

    # First line of user's address
    address_line1 = StringField('Address Line 1', validators=[DataRequired()])

    # Second line of user's address (optional)
    address_line2 = StringField('Address Line 2 (Optional)')

    # User's city
    city = StringField('City', validators=[DataRequired()])

    # User's country
    country = StringField('Country', validators=[DataRequired()])

    # User's postcode
    postcode = StringField('Postcode', validators=[DataRequired()])

    # Selected subscription plan
    selected_plan = HiddenField('Selected Plan', validators=[DataRequired()])

    # User's password
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message="Password must be at least 6 characters long."),
            Regexp(
                r'^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$',
                message="Password must contain at least one uppercase letter, one digit, and one special character."
            )
        ]
    )

    # Confirm password
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )

    # Submit button
    submit = SubmitField("Register")


# =======================================================
# Check Email Exists Route (AJAX using SQL)
# =======================================================

# Handle AJAX requests to check if an email exists in the database
@register.route("/check_email", methods=["POST"])
@csrf.exempt
def check_email():
    """
    Check if an email already exists in SQL.
    Accepts JSON: { "email": "..." } and returns { "exists": bool }.
    """

    # Wrap handler for safety
    try:
        # Log incoming request basics
        logging.info("📩 Received request for email check")

        # Log raw request (useful while wiring up)
        logging.info("🔍 Raw Request Data: %s", request.get_data(as_text=True))
        logging.info("🔍 Request Headers: %s", dict(request.headers))

        # Ensure JSON body
        if not request.is_json:
            return jsonify({"exists": False, "message": "⚠ Invalid request format. Expected JSON."}), 400

        # Parse + normalize email
        data = request.get_json(silent=True) or {}
        email = (data.get("email") or "").strip().lower()
        if not email:
            return jsonify({"exists": False, "message": "⚠ Email field is required."}), 400

        # Create SQL session
        sql_session = SessionLocal()
        try:
            # Case-insensitive lookup against SQL
            found = (
                sql_session.query(UserSQL.id)
                           .filter(func.lower(UserSQL.email) == email)
                           .first()
                is not None
            )
        finally:
            # Always close session
            sql_session.close()

        # Return existence result
        if found:
            return jsonify({"exists": True, "message": "❌ This email is already registered. Try logging in instead."}), 200

        # Email available
        return jsonify({"exists": False, "message": "✅ Email available."}), 200

    # Unexpected server errors
    except Exception as e:
        logging.error("check_email error: %s", e, exc_info=True)
        return jsonify({"exists": False, "message": "⚠ Server error."}), 500


# =======================================================
# Register User Route
# =======================================================

# Handle GET to display the form and POST to create a user in SQL
@register.route('/register', methods=['GET', 'POST'])
def register_user():
    # Instantiate the registration form
    form = RegisterForm()

    # Process only when the request method is POST
    if request.method == "POST":
        # Log basic diagnostics
        logging.info("✅ Received POST request for /register")

        # Log raw form payload for debugging
        logging.info("🔹 Raw Form Data: %s", request.form)

        # Log CSRF presence for debugging
        if 'csrf_token' in request.form:
            logging.info("🔹 CSRF Token Received: %s", request.form['csrf_token'])
        else:
            logging.warning("❌ No CSRF Token Found!")

        # Clear any existing flash messages before validation
        session.pop('_flashes', None)

        # Validate CSRF and field validators
        if form.validate_on_submit():
            # Wrap the main registration logic for clear error handling
            try:
                # Extract key fields from form
                first_name = form.first_name.data.strip()
                last_name = form.last_name.data.strip()
                username = f"{first_name} {last_name}"
                email = form.email.data.strip().lower()
                password = form.password.data.strip()
                selected_plan = form.selected_plan.data.strip() if form.selected_plan.data else None

                # Ensure a plan is selected
                if not selected_plan:
                    logging.error("❌ No plan selected!")
                    flash("⚠️ Please select a plan before registering.", 'danger')
                    return render_template('register.html', form=form)

                # Open SQL session
                sql_session = SessionLocal()
                try:
                    # Check for duplicate email
                    existing = sql_session.query(UserSQL).filter(UserSQL.email == email).one_or_none()
                    if existing:
                        logging.warning("❌ Email %s already exists in database", email)
                        flash("❌ This email is already registered. Try logging in instead.", 'danger')
                        return redirect(url_for('register.register_user'))

                    # Hash the password
                    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

                    # Create a new user record
                    new_user = UserSQL(
                        username=username,
                        email=email,
                        password=hashed_password,
                        role="user",
                        created_at=datetime.utcnow(),
                    )

                    # Persist the new user to the database
                    sql_session.add(new_user)
                    sql_session.commit()

                # Handle unique/constraint violations
                except IntegrityError as ie:
                    sql_session.rollback()
                    logging.error("IntegrityError during registration: %s", ie, exc_info=True)
                    flash("❌ Email already exists or data invalid.", "danger")
                    return redirect(url_for('register.register_user'))

                # Handle generic SQL errors
                except SQLAlchemyError as se:
                    sql_session.rollback()
                    logging.error("SQLAlchemyError during registration: %s", se, exc_info=True)
                    flash("❌ Database error. Please try again.", "danger")
                    return redirect(url_for('register.register_user'))

                # Ensure session is closed
                finally:
                    sql_session.close()

                # Indicate successful registration
                flash("Registration successful! You selected: " + selected_plan + ".", "success")
                return jsonify({"success": True, "message": "Registration successful!"}), 200

            # Handle unexpected server errors during registration
            except Exception as e:
                logging.error("Unexpected error during registration: %s", e, exc_info=True)
                flash("❌ Registration failed. Please try again.", 'danger')
                return redirect(url_for('register.register_user'))

        # Handle validation failures (stay on form with messages)
        else:
            return render_template('register.html', form=form)

    # Render registration template for GET requests
    return render_template('register.html', form=form, show_success=request.args.get("success") == "true")
