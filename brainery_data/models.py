from flask_login import UserMixin
from bson.objectid import ObjectId
from brainery_data import mongo

class User(UserMixin):
    """User model for authentication and session handling."""

    def __init__(self, user_data):
        """Initialize the user with MongoDB data."""
        self.id = str(user_data["_id"])  # Convert ObjectId to string for Flask-Login
        self.username = user_data["username"]
        self.email = user_data["email"]
        self.password = user_data["password"]  # Hashed password

    @staticmethod
    def find_by_email(email):
        """Find a user by email and return a User object."""
        user_data = mongo.db.users.find_one({"email": email})
        return User(user_data) if user_data else None

    @staticmethod
    def find_by_id(user_id):
        """Find a user by ID and return a User object."""
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User(user_data) if user_data else None

    def save(self):
        """Save a new user to the MongoDB database."""
        return mongo.db.users.insert_one({
            "username": self.username,
            "email": self.email,
            "password": self.password  # Make sure password is hashed
        })

class Resource:
    """Model for learning resources contributed by users."""

    def __init__(self, title, description, link, category, user_id):
        """Initialize a resource object."""
        self.title = title
        self.description = description
        self.link = link
        self.category = category
        self.user_id = user_id  # Store user ID as a string

    def save(self):
        """Save the resource to the MongoDB collection."""
        return mongo.db.resources.insert_one(self.__dict__)

    @staticmethod
    def find_all():
        """Retrieve all resources."""
        return list(mongo.db.resources.find())

    @staticmethod
    def find_by_id(resource_id):
        """Retrieve a single resource by ID."""
        return mongo.db.resources.find_one({"_id": ObjectId(resource_id)})

    @staticmethod
    def find_by_category(category):
        """Retrieve resources filtered by category."""
        return list(mongo.db.resources.find({"category": category}))

    @staticmethod
    def delete(resource_id):
        """Delete a resource by ID."""
        return mongo.db.resources.delete_one({"_id": ObjectId(resource_id)})

    @staticmethod
    def update(resource_id, updated_data):
        """Update a resource by ID."""
        return mongo.db.resources.update_one({"_id": ObjectId(resource_id)}, {"$set": updated_data})
