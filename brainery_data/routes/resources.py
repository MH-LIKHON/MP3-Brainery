from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from brainery_data import mongo

resource = Blueprint("resource", __name__)

@resource.route("/add", methods=["GET", "POST"])
@login_required
def add_resource():
    """Allow users to add a new learning resource."""
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        link = request.form.get("link")
        category = request.form.get("category")

        mongo.db.resources.insert_one({
            "title": title,
            "description": description,
            "link": link,
            "category": category,
            "user_id": current_user.id
        })

        flash("Resource added successfully!", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("add_resource.html")

@resource.route("/edit/<resource_id>", methods=["GET", "POST"])
@login_required
def edit_resource(resource_id):
    """Allow users to edit an existing resource."""
    resource_data = mongo.db.resources.find_one({"_id": ObjectId(resource_id)})

    if not resource_data or resource_data["user_id"] != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        updated_data = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "link": request.form.get("link"),
            "category": request.form.get("category")
        }

        mongo.db.resources.update_one({"_id": ObjectId(resource_id)}, {"$set": updated_data})
        flash("Resource updated successfully!", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("edit_resource.html", resource=resource_data)

@resource.route("/delete/<resource_id>")
@login_required
def delete_resource(resource_id):
    """Allow users to delete a resource."""
    resource_data = mongo.db.resources.find_one({"_id": ObjectId(resource_id)})

    if not resource_data or resource_data["user_id"] != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("dashboard.index"))

    mongo.db.resources.delete_one({"_id": ObjectId(resource_id)})
    flash("Resource deleted successfully!", "success")
    return redirect(url_for("dashboard.index"))
