# =======================================================
# Resource Management Routes
# =======================================================

# Import Flask primitives
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Import login helpers
from flask_login import login_required, current_user

# Import database session and model
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import ResourceSQL


# =======================================================
# Initialize Resource Blueprint
# =======================================================

# Create the resource blueprint (no prefix; routes specify full paths)
resource = Blueprint("resource", __name__)


# =======================================================
# Add a Resource
# =======================================================

@resource.route("/add", methods=["GET", "POST"])
@login_required
def add_resource():
    """Allow users to add a new learning resource."""

    # Process HTML form submit
    if request.method == "POST":
        # Extract fields from form
        title = (request.form.get("title") or "").strip()
        description = (request.form.get("description") or "").strip()
        link = (request.form.get("link") or "").strip()
        category = (request.form.get("category") or "").strip()

        # Validate required fields
        if not title:
            flash("Title is required.", "danger")
            return render_template("add_resource.html")

        # Convert session id (string) to int PK
        try:
            uid = int(current_user.id)
        except (TypeError, ValueError):
            flash("Invalid user context.", "danger")
            return render_template("add_resource.html")

        # Open DB session and insert the resource
        db = SessionLocal()
        try:
            # Create ORM row
            row = ResourceSQL(
                title=title,
                description=description,
                link=link,
                category=category,
                user_id=uid,
            )

            # Persist to database
            db.add(row)
            db.commit()

            # User feedback and redirect
            flash("Resource added successfully!", "success")
            return redirect(url_for("dashboard.dashboard_main"))

        except Exception as e:
            # Rollback on failure
            db.rollback()
            flash("Failed to add resource. Please try again.", "danger")
            return render_template("add_resource.html")

        finally:
            # Ensure session is closed
            db.close()

    # Render the creation form
    return render_template("add_resource.html")


# =======================================================
# Edit a Resource
# =======================================================

@resource.route("/edit/<int:resource_id>", methods=["GET", "POST"])
@login_required
def edit_resource(resource_id):
    """Allow users to edit an existing resource."""

    # Convert session id (string) to int PK
    try:
        uid = int(current_user.id)
    except (TypeError, ValueError):
        flash("Invalid user context.", "danger")
        return redirect(url_for("dashboard.dashboard_main"))

    # Open DB session
    db = SessionLocal()
    try:
        # Fetch the resource row
        row = db.get(ResourceSQL, resource_id)

        # Ensure resource exists and belongs to current user
        if not row or row.user_id != uid:
            flash("Unauthorized action!", "danger")
            return redirect(url_for("dashboard.dashboard_main"))

        # Handle form submission
        if request.method == "POST":
            # Update fields from form
            row.title = (request.form.get("title") or "").strip()
            row.description = (request.form.get("description") or "").strip()
            row.link = (request.form.get("link") or "").strip()
            row.category = (request.form.get("category") or "").strip()

            # Validate title
            if not row.title:
                flash("Title is required.", "danger")
                return render_template("edit_resource.html", resource=row)

            # Commit the update
            db.commit()
            flash("Resource updated successfully!", "success")
            return redirect(url_for("dashboard.dashboard_main"))

        # GET: render the edit form with current data
        return render_template("edit_resource.html", resource=row)

    except Exception as e:
        # Rollback on failure and report
        db.rollback()
        flash("Failed to update resource. Please try again.", "danger")
        return redirect(url_for("dashboard.dashboard_main"))

    finally:
        # Close session
        db.close()


# =======================================================
# Delete a Resource
# =======================================================

@resource.route("/delete/<int:resource_id>")
@login_required
def delete_resource(resource_id):
    """Allow users to delete a resource."""

    # Convert session id (string) to int PK
    try:
        uid = int(current_user.id)
    except (TypeError, ValueError):
        flash("Invalid user context.", "danger")
        return redirect(url_for("dashboard.dashboard_main"))

    # Open DB session
    db = SessionLocal()
    try:
        # Fetch the resource row
        row = db.get(ResourceSQL, resource_id)

        # Ensure resource exists and belongs to current user
        if not row or row.user_id != uid:
            flash("Unauthorized action!", "danger")
            return redirect(url_for("dashboard.dashboard_main"))

        # Delete and commit
        db.delete(row)
        db.commit()

        # Notify and return to dashboard
        flash("Resource deleted successfully!", "success")
        return redirect(url_for("dashboard.dashboard_main"))

    except Exception as e:
        # Rollback on error
        db.rollback()
        flash("Failed to delete resource. Please try again.", "danger")
        return redirect(url_for("dashboard.dashboard_main"))

    finally:
        # Close session
        db.close()