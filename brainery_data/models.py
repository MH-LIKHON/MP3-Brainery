import logging
from flask_login import UserMixin
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# Set up logging
logging.basicConfig(level=logging.ERROR)


class User(UserMixin):
    """User model for authentication and session handling."""

    def __init__(self, user_data):
        """Initialize the user with MongoDB data."""
        self.id = str(user_data.get("_id", ""))
        self.username = user_data.get("username", "").strip()
        self.first_name = user_data.get("first_name", "").strip()
        self.last_name = user_data.get("last_name", "").strip()
        self.email = user_data.get("email", "").strip().lower()
        self.password = user_data.get("password", "")
        self.phone = user_data.get("phone", "").strip()
        self.dob = user_data.get("dob", "") if user_data.get("dob") else "N/A"
        self.address_line1 = user_data.get("address_line1", "").strip()
        self.address_line2 = user_data.get("address_line2", "") or ""
        self.city = user_data.get("city", "").strip()
        self.country = user_data.get("country", "").strip()
        self.postcode = user_data.get("postcode", "").strip()
        self.selected_plan = user_data.get("selected_plan", "").strip()

    @staticmethod
    def find_by_email(email, mongo):
        """Find a user by email (case-insensitive) and return a User object."""
        try:
            user_data = mongo.db.users.find_one(
                {"email": {"$regex": f"^{email.strip()}$", "$options": "i"}})
            return User(user_data) if user_data else None
        except Exception as e:
            logging.error(f"❌ Error finding user by email {email}: {e}")
            return None

    @staticmethod
    def find_by_id(user_id, mongo):
        """Find a user by ID and return a User object."""
        try:
            obj_id = ObjectId(user_id)
            user_data = mongo.db.users.find_one({"_id": obj_id})
            return User(user_data) if user_data else None
        except Exception as e:
            logging.error(f"❌ Error finding user by ID {user_id}: {e}")
            return None

    def save(self, mongo):
        """Save a new user to MongoDB."""
        # Ensure required fields are present
        if not self.username or not self.email or not self.password or not self.selected_plan:
            logging.error(
                "❌ User registration failed: Missing required fields.")
            return None

        # Prevent duplicate username and email registrations
        if mongo.db.users.find_one({"username": self.username}) or mongo.db.users.find_one({"email": self.email.lower()}):
            logging.error(
                f"❌ Duplicate registration attempt: Username or Email already exists ({self.email}).")
            return None

        # Ensure the password is securely hashed
        if not self.password or not self.password.startswith("pbkdf2:"):
            self.password = generate_password_hash(
                self.password, method="pbkdf2:sha256")

        # Prepare user data
        user_data = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email.lower(),
            "password": self.password,
            "phone": self.phone,
            "dob": self.dob,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "city": self.city,
            "country": self.country,
            "postcode": self.postcode,
            "selected_plan": self.selected_plan
        }

        # Insert the user into the database and return the inserted user ID
        try:
            inserted = mongo.db.users.insert_one(user_data)
            return str(inserted.inserted_id)
        except Exception as e:
            logging.error(f"❌ Error saving user {self.email}: {e}")
            return None

    def check_password(self, password):
        """Check if the provided password matches the stored hashed password."""
        return check_password_hash(self.password, password)


class Resource:
    """Model for learning resources contributed by users."""

    def __init__(self, title, description, link, category, user_id):
        """Initialize a resource object."""
        self.title = title
        self.description = description
        self.link = link
        self.category = category
        self.user_id = str(user_id)

    def save(self, mongo):
        """Save the resource to MongoDB."""
        try:
            inserted = mongo.db.resources.insert_one(self.__dict__)
            return str(inserted.inserted_id)
        except Exception as e:
            logging.error(f"❌ Error saving resource: {e}")
            return None

    @staticmethod
    def find_by_id(resource_id, mongo):
        """Retrieve a single resource by ID."""
        try:
            obj_id = ObjectId(resource_id)
            return mongo.db.resources.find_one({"_id": obj_id})
        except Exception as e:
            logging.error(f"❌ Error finding resource by ID {resource_id}: {e}")
            return None

    @staticmethod
    def delete(resource_id, mongo):
        """Delete a resource by ID."""
        try:
            obj_id = ObjectId(resource_id)
            result = mongo.db.resources.delete_one({"_id": obj_id})
            return result.deleted_count > 0
        except Exception as e:
            logging.error(
                f"❌ Error deleting resource by ID {resource_id}: {e}")
            return False

    @staticmethod
    def update(resource_id, updated_data, mongo):
        """Update a resource by ID."""
        try:
            obj_id = ObjectId(resource_id)

            # Ensure only valid fields are updated
            valid_fields = {"title", "description", "link", "category"}
            updated_data = {k: v for k,
                            v in updated_data.items() if k in valid_fields}

            result = mongo.db.resources.update_one(
                {"_id": obj_id}, {"$set": updated_data})
            return result.modified_count > 0
        except Exception as e:
            logging.error(
                f"❌ Error updating resource by ID {resource_id}: {e}")
            return False
