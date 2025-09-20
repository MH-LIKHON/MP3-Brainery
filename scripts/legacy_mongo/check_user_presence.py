import os
from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import func
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import UserSQL

load_dotenv(".env")

# Normalise email (case-insensitive check)
email = "TA2@gamil.com".strip().lower()

# --- SQL check ---
s = SessionLocal()
try:
    u = s.query(UserSQL).filter(func.lower(UserSQL.email) == email).one_or_none()
    print("SQL =", "FOUND" if u else "NOT FOUND", "-", (u.email if u else None))
finally:
    s.close()

# --- Mongo check ---
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, serverSelectionTimeoutMS=8000)
db = client.get_default_database()
doc = db.users.find_one({"email": email})
print("Mongo =", "FOUND" if doc else "NOT FOUND")
