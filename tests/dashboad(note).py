from flask import Blueprint, render_template
from flask_login import login_required, current_user
from brainery_data import mongo

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
@login_required
def dashboard_home():
    """Render the user dashboard."""
    user_resources = list(mongo.db.resources.find(
        {"user_id": current_user.id}))
    return render_template("dashboard.html", resources=user_resources)


----------


(This is the code from 06 March 2025 at 00: 12)
