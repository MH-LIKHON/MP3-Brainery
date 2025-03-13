import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import pymongo
from brainery_data import mongo, csrf

# ===========================
# 🔹 LOGGING SETUP
# ===========================
logging.basicConfig(level=logging.INFO)  # Change to DEBUG if needed

# ===========================
# 🔹 INITIALIZE BLUEPRINT
# ===========================
register = Blueprint('register', __name__)

# ===========================
# 🔹 REGISTRATION FORM CLASS
# ===========================


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address_line1 = StringField('Address Line 1', validators=[DataRequired()])
    address_line2 = StringField('Address Line 2 (Optional)')
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])
    selected_plan = HiddenField('Selected Plan', validators=[DataRequired()])

    # ✅ Secure Password Field
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters long."),
        Regexp(r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]+$',
               message="Password must contain at least one uppercase letter, one digit, and one special character.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])

    submit = SubmitField("Register")


# ===========================
# 🔹 CHECK EMAIL EXISTS ROUTE (AJAX)
# ===========================

@register.route('/check_email', methods=['POST'])
@csrf.exempt  # ✅ Ensure CSRF is disabled for this route
def check_email():
    """Check if email already exists in the database (AJAX Request)"""
    try:
        logging.info("📩 Received request for email check")

        # Log request data for debugging
        logging.info(f"🔍 Raw Request Data: {request.get_data(as_text=True)}")
        logging.info(f"🔍 Request Headers: {request.headers}")

        # ✅ Ensure request is JSON
        if not request.is_json:
            logging.error("⚠ Invalid request format (not JSON)")
            return jsonify({"exists": False, "message": "⚠ Invalid request format. Expected JSON."}), 400

        data = request.get_json()

        # ✅ Ensure 'email' key exists
        if "email" not in data:
            logging.error("⚠ Missing 'email' in request data")
            return jsonify({"exists": False, "message": "⚠ Email field is required."}), 400

        email = data["email"].strip().lower()
        logging.info(f"🔍 Checking email: {email}")

        # ✅ Ensure MongoDB is active
        if mongo.db is None:
            logging.error("❌ MongoDB connection is missing!")
            return jsonify({"success": False, "message": "⚠ Database error. Try again later."}), 500
        else:
            logging.info("✅ MongoDB Connection Active")

        # ✅ Check if email exists in database
        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            logging.info(f"❌ Email {email} already registered")
            return jsonify({"exists": True, "message": "❌ This email is already registered. Try logging in instead."}), 200

        logging.info(f"✅ Email {email} is available")
        return jsonify({"exists": False, "message": "✅ Email available."}), 200

    except Exception as e:
        logging.error(f"❌ Server error: {str(e)}")
        return jsonify({"exists": False, "message": f"⚠ Server error: {str(e)}"}), 500


# ===========================
# 🔹 REGISTER USER ROUTE
# ===========================

@register.route('/register', methods=['GET', 'POST'])
def register_user():
    """Handles User Registration"""
    form = RegisterForm()

    logging.info(f"🔎 Request method: {request.method}")

    if request.method == "POST":
        logging.info("✅ Received POST request!")
        logging.info(f"🔹 Raw Form Data: {request.form}")  # Log full form data

        # Manually log CSRF token if applicable
        if 'csrf_token' in request.form:
            logging.info(
                f"🔹 CSRF Token Received: {request.form['csrf_token']}")
        else:
            logging.warning("❌ No CSRF Token Found!")

        # Clear previous flash messages before setting new ones
        session.pop('_flashes', None)

        if form.validate_on_submit():  # This is where validation might fail
            logging.info("✅ Registration form validated successfully!")

            try:
                first_name = form.first_name.data.strip()
                last_name = form.last_name.data.strip()
                username = f"{first_name} {last_name}"
                email = form.email.data.strip().lower()
                password = form.password.data.strip()
                selected_plan = form.selected_plan.data.strip() if form.selected_plan.data else None

                logging.info(
                    f"📌 Extracted Data - Username: {username}, Email: {email}, Plan: {selected_plan}")

                if not selected_plan:
                    logging.error("❌ No plan selected!")
                    flash("⚠️ Please select a plan before registering.", 'danger')
                    return render_template('register.html', form=form)

                # Check if email already exists
                existing_user = mongo.db.users.find_one({"email": email})
                if existing_user:
                    logging.warning(f"❌ Email {email} already exists in DB!")
                    flash(
                        "❌ This email is already registered. Try logging in instead.", 'danger')
                    return redirect(url_for('register.register_user'))

                dob_str = form.dob.data.strftime(
                    "%Y-%m-%d") if form.dob.data else "N/A"
                hashed_password = generate_password_hash(
                    password, method="pbkdf2:sha256")

                user_data = {
                    "username": username,
                    "email": email,
                    "password": hashed_password,
                    "phone": form.phone.data.strip(),
                    "address_line1": form.address_line1.data.strip(),
                    "address_line2": form.address_line2.data.strip() if form.address_line2.data else None,
                    "city": form.city.data.strip(),
                    "country": form.country.data.strip(),
                    "postcode": form.postcode.data.strip(),
                    "dob": dob_str,
                    "selected_plan": selected_plan,
                    "created_at": datetime.utcnow()
                }

                logging.info(
                    f"🔄 Attempting to insert user into MongoDB: {user_data}")

                # Ensure MongoDB connection is active before inserting
                if mongo.db is None:
                    logging.error(
                        "❌ MongoDB connection is missing! Aborting registration.")
                    flash("⚠ Database error. Please try again later.", 'danger')
                    return redirect(url_for('register.register_user'))

                insert_result = mongo.db.users.insert_one(user_data)

                if insert_result.inserted_id:
                    logging.info(
                        f"✅ User {email} successfully saved in MongoDB with ID: {insert_result.inserted_id}")
                    flash(
                        f"🎉 Registration successful! You selected: {selected_plan}.", 'success')

                    return jsonify({"success": True, "message": "Registration successful!"}), 200
                else:
                    logging.error("❌ MongoDB insert operation failed!")
                    flash("❌ Registration failed. Please try again.", 'danger')
                    return redirect(url_for('register.register_user'))

            except pymongo.errors.DuplicateKeyError:
                logging.warning(f"❌ Email {email} already exists!")
                flash(
                    "❌ This email is already registered. Try logging in instead.", 'danger')
                return redirect(url_for('register.register_user'))
            except Exception as e:
                logging.error(
                    f"❌ Unexpected error during registration: {str(e)}")
                flash("❌ Registration failed. Please try again.", 'danger')
                return redirect(url_for('register.register_user'))

    return render_template('register.html', form=form, show_success=request.args.get("success") == "true")
