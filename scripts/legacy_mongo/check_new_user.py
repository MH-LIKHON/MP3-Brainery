from brainery_data import create_app, mongo
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import UserSQL

EMAIL = "NEW_EMAIL_HERE"

def main():
    print("=== Check SQL ===")
    db = SessionLocal()
    try:
        u = db.query(UserSQL).filter(UserSQL.email == EMAIL).one_or_none()
        print("SQL user exists:", bool(u))
        if u:
            print(f"SQL role={u.role} username={u.username}")
    finally:
        db.close()

    print("\n=== Check Mongo ===")
    app = create_app()
    with app.app_context():
        doc = mongo.db.users.find_one({"email": {"$regex": f"^{EMAIL}$", "$options": "i"}})
        print("Mongo user exists:", bool(doc))
        if doc:
            print(f"Mongo role={doc.get('role') or 'user'} username={doc.get('username')}")
if __name__ == "__main__":
    main()
