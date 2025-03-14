# =======================================================
# Resource Management Routes
# =======================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from brainery_data import mongo

# Initialize the blueprint for resource-related routes
resource = Blueprint("resource", __name__)

# =======================================================
# Add a Resource
# =======================================================


@resource.route("/add", methods=["GET", "POST"])
@login_required
def add_resource():
    """Allow users to add a new learning resource."""
    if request.method == "POST":
        # Retrieve form data
        title = request.form.get("title")
        description = request.form.get("description")
        link = request.form.get("link")
        category = request.form.get("category")

        # Insert the new resource into the MongoDB collection
        mongo.db.resources.insert_one({
            "title": title,
            "description": description,
            "link": link,
            "category": category,
            "user_id": current_user.id
        })

        # Flash a success message and redirect to the dashboard
        flash("Resource added successfully!", "success")
        return redirect(url_for("dashboard.index"))

    # Render the resource creation form template
    return render_template("add_resource.html")

# =======================================================
# Edit a Resource
# =======================================================


@resource.route("/edit/<resource_id>", methods=["GET", "POST"])
@login_required
def edit_resource(resource_id):
    """Allow users to edit an existing resource."""
    # Retrieve the resource data from the database
    resource_data = mongo.db.resources.find_one({"_id": ObjectId(resource_id)})

    # Ensure the current user owns the resource before proceeding
    if not resource_data or resource_data["user_id"] != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        # Update resource data with form input
        updated_data = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "link": request.form.get("link"),
            "category": request.form.get("category")
        }

        # Update the resource in the database
        mongo.db.resources.update_one(
            {"_id": ObjectId(resource_id)}, {"$set": updated_data})

        # Flash a success message and redirect to the dashboard
        flash("Resource updated successfully!", "success")
        return redirect(url_for("dashboard.index"))

    # Render the resource editing form template
    return render_template("edit_resource.html", resource=resource_data)

# =======================================================
# Delete a Resource
# =======================================================


@resource.route("/delete/<resource_id>")
@login_required
def delete_resource(resource_id):
    """Allow users to delete a resource."""
    # Retrieve the resource data from the database
    resource_data = mongo.db.resources.find_one({"_id": ObjectId(resource_id)})

    # Ensure the current user owns the resource before proceeding
    if not resource_data or resource_data["user_id"] != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("dashboard.index"))

    # Delete the resource from the database
    mongo.db.resources.delete_one({"_id": ObjectId(resource_id)})

    # Flash a success message and redirect to the dashboard
    flash("Resource deleted successfully!", "success")
    return redirect(url_for("dashboard.index"))
