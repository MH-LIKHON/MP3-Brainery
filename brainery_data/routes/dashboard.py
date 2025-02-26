from flask import Blueprint, render_template
from flask_login import login_required, current_user
from brainery_data import mongo

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
@login_required
def index():
    """Render the user dashboard."""
    user_resources = list(mongo.db.resources.find({"user_id": current_user.id}))
    return render_template("dashboard.html", resources=user_resources)
