import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import func
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import UserSQL

load_dotenv(".env")

EMAIL = "TA2@gamil.com".strip().lower()

# --- Mongo: fetch source doc ---
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, serverSelectionTimeoutMS=8000)
db = client.get_default_database()
src = db.users.find_one({"email": EMAIL})
if not src:
    print("Mongo: NOT FOUND:", EMAIL)
    raise SystemExit(0)

# Prepare fields
username = src.get("username") or (src.get("first_name","").strip() + " " + src.get("last_name","").strip()).strip() or EMAIL
hashed_password = src.get("password") or ""
roles = src.get("roles") or []
role = "admin" if isinstance(roles, list) and "admin" in [r.lower() for r in roles if isinstance(r, str)] else "user"

# --- SQL: upsert ---
s = SessionLocal()
try:
    u = s.query(UserSQL).filter(func.lower(UserSQL.email) == EMAIL).one_or_none()
    if u:
        u.username = username
        if hashed_password:
            u.password = hashed_password
        u.role = role
        print(f"SQL: UPDATED -> {EMAIL} (role={role})")
    else:
        u = UserSQL(
            username=username,
            email=EMAIL,
            password=hashed_password or "!",  # keep not-empty; already hashed in Mongo
            role=role,
            created_at=datetime.utcnow(),
        )
        s.add(u)
        print(f"SQL: INSERTED -> {EMAIL} (role={role})")
    s.commit()
finally:
    s.close()
