from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from brainery_data import mongo
from brainery_data.models import User

# Initialize Blueprint for Register
register = Blueprint('register', __name__)

# Define the Registration Form here instead of importing it
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
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

@register.route('/register', methods=['GET', 'POST'])
def register_user():
    """Handle user registration."""
    form = RegisterForm()  # Initialize the form

    if form.validate_on_submit():  # Check if the form is submitted and validated
        # Extract data from form
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = f"{first_name} {last_name}"  # Combine first and last name to form a username
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match", 'danger')
            return redirect(url_for('register.register_user'))

        # Hash the password before saving it
        hashed_password = generate_password_hash(password)

        # Check if email already exists in the database
        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            flash("Email already registered", 'danger')
            return redirect(url_for('register.register_user'))

        # Prepare the user data
        user = User({
            "username": username,
            "email": email,
            "password": hashed_password,
            "phone": form.phone.data,
            "address_line1": form.address_line1.data,
            "address_line2": form.address_line2.data,
            "city": form.city.data,
            "country": form.country.data,
            "postcode": form.postcode.data,
            "dob": form.dob.data
        })
        
        user.save(mongo)  # Pass mongo here when saving

        flash("Registration successful! Please log in.", 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)
