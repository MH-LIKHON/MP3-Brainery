import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from datetime import datetime
from brainery_data import mongo
from brainery_data.models import User

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
# 🔹 LOGIN FORM CLASS
# ===========================
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


# ===========================
# 🔹 REGISTER USER ROUTE
# ===========================
@register.route('/register', methods=['GET', 'POST'])
def register_user():
    """Handles User Registration"""
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            # ✅ STEP 1: Extract & Sanitize Input Data
            first_name = form.first_name.data.strip()
            last_name = form.last_name.data.strip()
            username = f"{first_name} {last_name}"
            email = form.email.data.strip().lower()
            password = form.password.data.strip()
            selected_plan = form.selected_plan.data.strip()

            # ✅ DEBUG: Print registration data before saving
            print("✅ Registration form submitted successfully!")
            print(
                f"📌 Username: {username}, Email: {email}, Plan: {selected_plan}")

            # ✅ STEP 2: Ensure a Plan is Selected
            if not selected_plan:
                print("❌ No plan selected!")
                flash("⚠️ Please select a plan before registering.", 'danger')
                return redirect(url_for('register.register_user'))

            # ✅ STEP 3: Check if Email Already Exists (Case-Insensitive)
            existing_user = mongo.db.users.find_one(
                {"email": {"$regex": f"^{email}$", "$options": "i"}})
            if existing_user:
                print(f"❌ Email already exists in DB: {email}")
                flash(
                    "❌ This email is already registered. Try logging in instead.", 'danger')
                return redirect(url_for('register.register_user'))

            # ✅ STEP 4: Format Date of Birth
            dob_str = form.dob.data.strftime(
                "%Y-%m-%d") if form.dob.data else "N/A"

            # ✅ STEP 5: Hash Password Securely Before Storing
            hashed_password = generate_password_hash(
                password, method="pbkdf2:sha256")

            # ✅ STEP 6: Prepare the User Data for Insertion
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
                "created_at": datetime.utcnow()  # Store timestamp
            }

            print("🔄 Attempting to save user to MongoDB:",
                  user_data)  # Debugging print

            # ✅ STEP 7: Attempt to Save User in MongoDB
            try:
                mongo.db.users.insert_one(user_data)
                logging.info(f"✅ New user registered: {email}")
                print(f"✅ User {email} saved successfully in MongoDB!")
            except Exception as e:
                print(f"❌ ERROR while saving user: {str(e)}")
                logging.error(
                    f"❌ User registration error: {str(e)}", exc_info=True)
                flash(
                    "❌ Registration failed due to a system error. Please try again later.", 'danger')
                return redirect(url_for('register.register_user'))

            # ✅ STEP 8: Registration Success Message
            flash(
                f"🎉 Registration successful! You selected: {selected_plan}. Please log in.", 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            logging.exception(
                f"Unexpected error during registration: {str(e)}")
            flash("❌ Registration failed. Please try again.", 'danger')
            return redirect(url_for('register.register_user'))

    # ✅ STEP 9: Render the Registration Page
    return render_template('register.html', form=form)
