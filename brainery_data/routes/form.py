# ===========================
# Flask Form Definitions
# ===========================

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

# ===========================
# Registration Form Class
# ===========================
# Form for collecting user registration details, such as personal
# information, address, and password. All fields include validation
# rules to ensure data integrity.


class RegisterForm(FlaskForm):
    """Registration form for new users."""

    # User's first name
    first_name = StringField('First Name', validators=[DataRequired()])

    # User's last name
    last_name = StringField('Last Name', validators=[DataRequired()])

    # User's date of birth
    dob = DateField('Date of Birth', validators=[DataRequired()])

    # User's email address
    email = StringField('Email Address', validators=[DataRequired(), Email()])

    # User's phone number
    phone = StringField('Phone Number', validators=[DataRequired()])

    # Address line 1
    address_line1 = StringField('Address Line 1', validators=[DataRequired()])

    # Address line 2 (optional)
    address_line2 = StringField('Address Line 2 (Optional)')

    # User's city
    city = StringField('City', validators=[DataRequired()])

    # User's country
    country = StringField('Country', validators=[DataRequired()])

    # User's postcode
    postcode = StringField('Postcode', validators=[DataRequired()])

    # Plan the user selected (hidden field)
    selected_plan = HiddenField('Selected Plan', validators=[DataRequired()])

    # Password field with strong validation requirements
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters long."),
        Regexp(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
               message="Password must contain at least one uppercase letter, one digit, and one special character.")
    ])

    # Confirm password field to ensure both passwords match
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])

    # Submit button to register the user
    submit = SubmitField("Register")

# ===========================
# Login Form Class
# ===========================
# Form for user login, requiring only email and password fields.
# Includes basic validation to ensure proper credentials.


class LoginForm(FlaskForm):
    """Login form for existing users."""

    # Email field with validation for proper format
    email = StringField("Email", validators=[DataRequired(), Email()])

    # Password field
    password = PasswordField("Password", validators=[DataRequired()])

    # Submit button to log in
    submit = SubmitField("Login")
