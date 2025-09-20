from brainery_data import create_app, mongo
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import UserSQL
from werkzeug.security import generate_password_hash

def pick_admin_or_first():
    u = mongo.db.users.find_one({"role": {"$regex": "^admin$", "$options": "i"}})
    if not u:
        u = mongo.db.users.find_one()
    return u

def run_seed():
    src = pick_admin_or_first()
    if not src:
        print("No Mongo user found to seed.")
        return

    email = (src.get("email", "") or "").strip().lower()
    username = src.get("username", "") or (src.get("first_name","") + " " + src.get("last_name","")).strip() or email
    role = (src.get("role") or "user").lower()
    pw = src.get("password", "")

    # If the Mongo password was plain (unlikely), hash it. Otherwise reuse the hash string.
    if not pw or not any(pw.startswith(p) for p in ("pbkdf2:", "scrypt:", "bcrypt$")):
        pw = generate_password_hash(pw or "ChangeMe123!")

    db = SessionLocal()
    try:
        existing = db.query(UserSQL).filter(UserSQL.email == email).one_or_none()
        if existing:
            print(f"User already exists in SQL: {email}")
            return
        user = UserSQL(username=username[:120], email=email[:255], password=pw[:255], role=role[:20])
        db.add(user)
        db.commit()
        print(f"Seeded SQL user: {email}  role={role}")
    finally:
        db.close()

def main():
    # Bootstrap Flask so mongo is initialised
    app = create_app()
    with app.app_context():
        run_seed()

if __name__ == "__main__":
    main()
