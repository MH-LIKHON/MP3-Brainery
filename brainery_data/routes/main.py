from flask import Blueprint, render_template
from brainery_data import mongo

main = Blueprint("main", __name__)

@main.route("/")
def index():
    """Render the home page with all resources."""
    resources = list(mongo.db.resources.find())
    return render_template("index.html", resources=resources)
