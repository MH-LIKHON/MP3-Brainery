from flask import Blueprint, render_template

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    """Render the dashboard index page."""
    return render_template('index.html', title="Dashboard")
