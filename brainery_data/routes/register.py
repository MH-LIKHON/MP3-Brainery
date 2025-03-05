import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from datetime import datetime
from brainery_data import mongo
from brainery_data.models import User
from brainery_data.routes.form import RegisterForm

# ===========================
# 🔹 LOGGING SETUP
# ===========================
logging.basicConfig(level=logging.ERROR)

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
        Regexp(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
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

    print(f"🔎 Request method: {request.method}")

    if request.method == "POST":
        print("✅ Received POST request!")  # ✅ Log when form submits
        # ✅ Print raw data for debugging
        print(f"🔹 Raw Form Data: {request.form}")

    # ✅ Only validate form on POST request
    if request.method == "POST" and form.validate_on_submit():
        print("✅ Registration form submitted successfully!")

        try:
            first_name = form.first_name.data.strip()
            last_name = form.last_name.data.strip()
            username = f"{first_name} {last_name}"
            email = form.email.data.strip().lower()
            password = form.password.data.strip()
            selected_plan = form.selected_plan.data.strip()

            print(
                f"📌 Extracted Data - Username: {username}, Email: {email}, Plan: {selected_plan}")

            if not selected_plan:
                print("❌ No plan selected!")
                flash("⚠️ Please select a plan before registering.", 'danger')
                return redirect(url_for('register.register_user'))

            existing_user = mongo.db.users.find_one(
                {"email": {"$regex": f"^{email}$", "$options": "i"}})
            if existing_user:
                print(f"❌ Email {email} already exists in DB!")
                flash(
                    "❌ This email is already registered. Try logging in instead.", 'danger')
                return redirect(url_for('register.register_user'))

            # ✅ DEBUG: Ensure date of birth is being captured properly
            if form.dob.data:
                dob_str = form.dob.data.strftime("%Y-%m-%d")
                print(f"📆 Date of Birth: {dob_str}")
            else:
                dob_str = "N/A"
                print("⚠️ No Date of Birth provided!")

            hashed_password = generate_password_hash(
                password, method="pbkdf2:sha256")

            # ✅ DEBUG: Confirm all extracted data before inserting into MongoDB
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

            print("🔄 Attempting to insert user into MongoDB:", user_data)

            # ✅ Attempt MongoDB Insertion
            insert_result = mongo.db.users.insert_one(user_data)

            if insert_result.inserted_id:
                print(f"✅ User {email} successfully saved in MongoDB!")
                flash(
                    f"🎉 Registration successful! You selected: {selected_plan}. Please log in.", 'success')
                return redirect(url_for('auth.login'))
            else:
                print("❌ MongoDB insert operation failed!")
                flash("❌ Registration failed. Please try again.", 'danger')

        except Exception as e:
            print(f"❌ Unexpected error during registration: {str(e)}")
            flash("❌ Registration failed. Please try again.", 'danger')

    else:
        print("❌ Form validation skipped (GET request) or validation failed!")

    return render_template('register.html', form=form)
