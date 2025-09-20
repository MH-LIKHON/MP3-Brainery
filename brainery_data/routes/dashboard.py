# =======================================================
# User Routes
# =======================================================

# Import Flask primitives for views, JSON responses, and redirects
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session

# Import login/session helpers
from flask_login import login_required, current_user, logout_user

# Import database session and models
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import Subject, Topic, SavedTopic


# =======================================================
# Initialize Dashboard Blueprint
# =======================================================

# Create the dashboard blueprint with URL prefix /dashboard
dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# =======================================================
# Dashboard Home Route (Main Dashboard)
# =======================================================

@dashboard.route("/")
@login_required
def dashboard_main():
    """Render the main dashboard page for logged-in users."""

    # Log who is visiting for diagnostic purposes
    print(f"🔍 Current User: {current_user} (ID: {current_user.id})")

    # Render the dashboard template (no DB access required here)
    return render_template("dashboard.html")


# =======================================================
# Retrieve All Subjects
# =======================================================

@dashboard.route("/subjects", methods=["GET"])
@login_required
def get_subjects():
    """Fetch all subjects from the database and return as JSON."""

    try:
        # Open a new SQLAlchemy session
        db = SessionLocal()
        try:
            # Query all subjects ordered by name (A→Z)
            rows = db.query(Subject).order_by(Subject.name.asc()).all()
        finally:
            # Ensure the session is closed even on errors
            db.close()

        # Shape results for the UI (keep _id as string for data attributes)
        subjects = [
            {"_id": str(s.id), "name": s.name, "icon": s.icon or ""}
            for s in rows
        ]

        # Return JSON payload
        return jsonify(subjects), 200

    except Exception as e:
        # Log the error and return a safe message
        print(f"🚨 Error Fetching Subjects (SQL): {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# =======================================================
# Retrieve Topics by Subject ID
# =======================================================

@dashboard.route("/topics/<subject_id>", methods=["GET"])
@login_required
def get_topics(subject_id):
    """Fetch topics for a specific subject and return titles/descriptions."""

    # Validate that the path parameter is a valid integer
    try:
        sid = int(subject_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid Subject ID"}), 400

    try:
        # Open a new SQLAlchemy session
        db = SessionLocal()
        try:
            # Query topics for the given subject id; order alphabetically by title
            rows = (
                db.query(Topic)
                  .filter(Topic.subject_id == sid)
                  .order_by(Topic.title.asc())
                  .all()
            )
        finally:
            # Always close the session
            db.close()

        # Reduce fields to what the UI expects
        topics = [
            {"title": t.title, "description": t.description or ""}
            for t in rows
        ]

        # Return JSON payload
        return jsonify(topics), 200

    except Exception as e:
        # Log the error and return a safe message
        print(f"🚨 Error Fetching Topics (SQL): {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# =======================================================
# Retrieve a Specific Saved Topic
# =======================================================

@dashboard.route("/get_topic/<topic_id>", methods=["GET"])
@login_required
def get_topic(topic_id):
    """Retrieve details for a specific saved topic belonging to the user."""

    # Validate that the path parameter is a valid integer
    try:
        tid = int(topic_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid Topic ID format"}), 400

    try:
        # Open a new SQLAlchemy session
        db = SessionLocal()
        try:
            # Fetch the saved topic by primary key
            row = db.get(SavedTopic, tid)

            # Enforce ownership: topic must belong to the current user
            if not row or str(row.user_id) != str(current_user.id):
                return jsonify({"error": "Topic not found"}), 404

            # Shape payload for the UI
            payload = {
                "_id": str(row.id),
                "title": row.title,
                "summary": row.summary or "No summary available.",
                "timestamp": (row.created_at.isoformat() if row.created_at else "Unknown Date"),
            }

            # Return JSON payload
            return jsonify(payload), 200

        finally:
            # Ensure the session is closed
            db.close()

    except Exception as e:
        # Log the error and return a safe message
        print(f"🚨 Error Fetching Topic (SQL): {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# =======================================================
# Save a New Topic
# =======================================================

@dashboard.route("/save_topic", methods=["POST"])
@login_required
def save_topic():
    """Save a topic title (and optional summary) into the user's saved list."""

    try:
        # Parse inbound JSON body
        data = request.get_json()
        print("🔍 Received Data from JS:", data)

        # Validate presence of title in payload
        if not data or "title" not in data:
            return jsonify({"error": "Invalid data - Title missing"}), 400

        # Normalise title value
        topic_title = (data["title"] or "").strip()
        if not topic_title:
            return jsonify({"error": "Invalid data - Title missing"}), 400

        # Convert current_user.id (string) → integer PK
        try:
            uid = int(current_user.id)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid user context"}), 400

        # Open a new SQLAlchemy session
        db = SessionLocal()
        try:
            # Prevent duplicate titles for the same user
            exists = (
                db.query(SavedTopic)
                  .filter(SavedTopic.user_id == uid, SavedTopic.title == topic_title)
                  .first()
            )
            if exists:
                return jsonify({"error": "Topic already saved!"}), 400

            # Try to derive a summary from Topic table by title (optional)
            src = db.query(Topic).filter(Topic.title == topic_title).first()
            summary = src.description if src and src.description else "No summary available."

            # Create and persist the SavedTopic record
            st = SavedTopic(user_id=uid, title=topic_title, summary=summary)
            db.add(st)
            db.commit()
            db.refresh(st)

            # Return success and the created record's id/timestamp
            return jsonify({
                "message": "Topic saved successfully!",
                "timestamp": (st.created_at.isoformat() if st.created_at else None),
                "_id": str(st.id),
            }), 201

        finally:
            # Ensure the session is closed
            db.close()

    except Exception as e:
        # Log the error and return a safe message
        print("🚨 Error saving topic (SQL):", str(e))
        return jsonify({"error": "Internal server error"}), 500


# =======================================================
# Retrieve Saved Study Topics
# =======================================================

@dashboard.route("/saved_topics", methods=["GET"])
@login_required
def get_saved_topics():
    """Fetch the current user's saved topics (most recent first)."""

    try:
        # Convert current_user.id (string) → integer PK
        try:
            uid = int(current_user.id)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid user context"}), 400

        # Open a new SQLAlchemy session
        db = SessionLocal()
        try:
            # Query all saved topics for the user, newest first
            rows = (
                db.query(SavedTopic)
                  .filter(SavedTopic.user_id == uid)
                  .order_by(SavedTopic.created_at.desc())
                  .all()
            )

            # Shape results for UI expectations
            payload = []
            for r in rows:
                payload.append({
                    "_id": str(r.id),   # keep property name for the frontend
                    "title": r.title,
                    "summary": r.summary or "No summary available.",
                    "timestamp": (r.created_at.isoformat() if r.created_at else "Unknown Date"),
                })

            # Log success for diagnostics
            print("Saved Topics Retrieved Successfully!")

            # Return JSON payload
            return jsonify(payload), 200

        finally:
            # Ensure the session is closed
            db.close()

    except Exception as e:
        # Log the error and return a safe message
        print("🚨 Error Fetching Saved Topics (SQL):", str(e))
        return jsonify({"error": "Internal Server Error"}), 500


# =======================================================
# Update a Saved Topic
# =======================================================

@dashboard.route("/update_topic/<topic_id>", methods=["PUT"])
@login_required
def update_topic(topic_id):
    """Rename a saved topic for the current user."""

    try:
        # Parse inbound JSON body
        data = request.get_json()

        # Extract and validate the new title
        new_title = (data.get("new_title") or "").strip()
        if not new_title:
            return jsonify({"error": "New title required"}), 400

        # Validate and normalise path/user ids
        try:
            tid = int(topic_id)
            uid = int(current_user.id)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid IDs"}), 400

        # Open a new SQLAlchemy session
        db = SessionLocal()
        try:
            # Fetch the saved topic and check ownership
            row = db.get(SavedTopic, tid)
            if not row or row.user_id != uid:
                return jsonify({"error": "Topic not found"}), 404

            # Update the title and commit
            row.title = new_title
            db.commit()

            # Return success
            return jsonify({"message": "Topic updated successfully!"}), 200

        finally:
            # Ensure the session is closed
            db.close()

    except Exception as e:
        # Log the error and return a safe message
        print(f"🚨 Error Updating Topic (SQL): {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# =======================================================
# Delete a Saved Topic (DELETE)
# =======================================================

@dashboard.route("/delete_topic/<topic_id>", methods=["DELETE"])
@login_required
def delete_topic(topic_id):
    """Delete a saved topic belonging to the current user."""

    try:
        # Validate and normalise path/user ids
        try:
            tid = int(topic_id)
            uid = int(current_user.id)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid Topic ID format"}), 400

        # Open a new SQLAlchemy session
        db = SessionLocal()
        try:
            # Fetch the topic and check ownership
            row = db.get(SavedTopic, tid)
            if not row or row.user_id != uid:
                return jsonify({"error": "Topic not found"}), 404

            # Delete the record and commit
            db.delete(row)
            db.commit()

            # Return success
            return jsonify({"message": "Topic deleted successfully!"}), 200

        finally:
            # Ensure the session is closed
            db.close()

    except Exception as e:
        # Log the error and return a safe message
        print(f"🚨 Error Deleting Topic (SQL): {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# =======================================================
# Logout User
# =======================================================

@dashboard.route("/auth/logout", methods=["POST", "GET"])
@login_required
def logout():
    """
    Log the user out and redirect to login.
    """
    try:
        # Terminate the Flask-Login session
        logout_user()

        # Clear the server-side session store
        session.clear()

        # Diagnostic log for visibility
        print("🔴 User session cleared.")

        # Return JSON for AJAX calls; redirect for normal navigation
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"message": "You have been logged out."}), 200

        # Redirect the user back to the login page
        return redirect(url_for("auth.login"))

    except Exception as e:
        # Log the error and return a safe message
        print(f"🚨 Logout Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500