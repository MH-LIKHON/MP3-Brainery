import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from datetime import datetime
import pymongo
from brainery_data import mongo

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
# 🔹 REGISTER USER ROUTE
# ===========================


@register.route('/register', methods=['GET', 'POST'])
def register_user():
    """Handles User Registration"""
    form = RegisterForm()

    logging.info(f"🔎 Request method: {request.method}")

    if request.method == "POST":
        logging.info("✅ Received POST request!")
        logging.info(f"🔹 Raw Form Data: {request.form}")

        if form.validate_on_submit():
            logging.info("✅ Registration form validated successfully!")

            try:
                # Extract form data
                first_name = form.first_name.data.strip()
                last_name = form.last_name.data.strip()
                username = f"{first_name} {last_name}"
                email = form.email.data.strip().lower()
                password = form.password.data.strip()
                selected_plan = form.selected_plan.data.strip() if form.selected_plan.data else None

                logging.info(
                    f"📌 Extracted Data - Username: {username}, Email: {email}, Plan: {selected_plan}")

                # Check if a plan was selected
                if not selected_plan:
                    logging.error("❌ No plan selected!")
                    flash("⚠️ Please select a plan before registering.", 'danger')
                    return redirect(url_for('register.register_user'))

                # Check if email already exists
                existing_user = mongo.db.users.find_one({"email": email})

                if existing_user:
                    logging.warning(f"❌ Email {email} already exists in DB!")
                    flash(
                        "❌ This email is already registered. Try logging in instead.", 'danger')
                    return redirect(url_for('register.register_user'))

                # Convert Date of Birth to string format
                dob_str = form.dob.data.strftime(
                    "%Y-%m-%d") if form.dob.data else "N/A"

                # Hash the password
                hashed_password = generate_password_hash(
                    password, method="pbkdf2:sha256")

                # Create user data dictionary
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

                # Insert the user data into the MongoDB database
                logging.info("🔄 Attempting to insert user into MongoDB...")
                insert_result = mongo.db.users.insert_one(user_data)

                if insert_result.inserted_id:
                    logging.info(
                        f"✅ User {email} successfully saved in MongoDB!")
                    flash(
                        f"🎉 Registration successful! You selected: {selected_plan}.", 'success')

                    # ✅ Redirect to Success Page
                    return render_template('register.html', form=form, show_success=True)

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

        else:
            logging.warning(f"❌ Form validation failed! Errors: {form.errors}")
            flash(f"❌ Form validation failed! Errors: {form.errors}", "danger")

    return render_template('register.html', form=form)

# ===========================
# 🔹 SUCCESS PAGE ROUTE
# ===========================


@register.route('/register/success', methods=['GET'])
def success():
    """Displays Registration Success Message"""
    return render_template('register_success.html', title="Registration Successful")
