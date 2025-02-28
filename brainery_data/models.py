from flask_login import UserMixin
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    """User model for authentication and session handling."""

    def __init__(self, user_data):
        """Initialize the user with MongoDB data."""
        self.id = str(user_data.get("_id", ""))  # Convert ObjectId to string for Flask-Login
        self.username = user_data.get("username", "")
        self.email = user_data.get("email", "")
        self.password = user_data.get("password", "")

    @staticmethod
    def find_by_email(email, mongo):
        """Find a user by email and return a User object."""
        user_data = mongo.db.users.find_one({"email": email})
        return User(user_data) if user_data else None  # Return User object or None if no user is found

    @staticmethod
    def find_by_id(user_id, mongo):
        """Find a user by ID and return a User object."""
        try:
            user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            return User(user_data) if user_data else None  # Return User object or None if not found
        except Exception as e:
            print(f"Error finding user by ID: {e}")
            return None  # Handle invalid ObjectId gracefully

    def save(self, mongo):
        """Save a new user to MongoDB."""
        hashed_password = generate_password_hash(self.password)
        
        # Prepare user data
        user_data = {
            "username": self.username,
            "email": self.email,
            "password": hashed_password
        }

        # Insert the user into the database and return the inserted user ID
        inserted = mongo.db.users.insert_one(user_data)
        return str(inserted.inserted_id)

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
        self.user_id = str(user_id)  # Ensure user_id is stored as a string

    def save(self, mongo):
        """Save the resource to MongoDB."""
        try:
            inserted = mongo.db.resources.insert_one(self.__dict__)
            return str(inserted.inserted_id)
        except Exception as e:
            print(f"Error saving resource: {e}")
            return None  # Gracefully handle error in resource saving

    @staticmethod
    def find_all(mongo):
        """Retrieve all resources."""
        try:
            return list(mongo.db.resources.find())
        except Exception as e:
            print(f"Error retrieving resources: {e}")
            return []  # Return an empty list in case of error

    @staticmethod
    def find_by_id(resource_id, mongo):
        """Retrieve a single resource by ID."""
        try:
            return mongo.db.resources.find_one({"_id": ObjectId(resource_id)})
        except Exception as e:
            print(f"Error finding resource by ID: {e}")
            return None  # Handle invalid ObjectId gracefully

    @staticmethod
    def find_by_category(category, mongo):
        """Retrieve resources filtered by category."""
        try:
            return list(mongo.db.resources.find({"category": category}))
        except Exception as e:
            print(f"Error finding resources by category: {e}")
            return []  # Return an empty list in case of error

    @staticmethod
    def delete(resource_id, mongo):
        """Delete a resource by ID."""
        try:
            return mongo.db.resources.delete_one({"_id": ObjectId(resource_id)})
        except Exception as e:
            print(f"Error deleting resource by ID: {e}")
            return None  # Gracefully handle error in deleting resource

    @staticmethod
    def update(resource_id, updated_data, mongo):
        """Update a resource by ID."""
        try:
            return mongo.db.resources.update_one({"_id": ObjectId(resource_id)}, {"$set": updated_data})
        except Exception as e:
            print(f"Error updating resource by ID: {e}")
            return None  # Gracefully handle error in updating resource
