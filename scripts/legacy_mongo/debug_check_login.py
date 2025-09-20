from brainery_data import create_app, mongo
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import UserSQL
from werkzeug.security import check_password_hash

TEST_PASSWORD = "Qwerty@12345"
CANDIDATE_EMAILS = ["m.l@live.co.uk", "30m.l@live.co.uk"]

def main():
    print("=== SQL USERS ===")
    db = SessionLocal()
    try:
        users = db.query(UserSQL).all()
        for u in users:
            ok = check_password_hash(u.password or "", TEST_PASSWORD)
            print(f"- id={u.id} email={u.email} role={getattr(u,'role',None)} "
                  f"hash_prefix={(u.password or '')[:12]}... matches_test={ok}")
    finally:
        db.close()

    print("\n=== MONGO USERS (by candidate emails) ===")
    app = create_app()
    with app.app_context():
        for em in CANDIDATE_EMAILS:
            doc = mongo.db.users.find_one({"email": {"$regex": f"^{em}$", "$options": "i"}})
            if doc:
                role = (doc.get("role") or doc.get("roles") or "user")
                print(f"- FOUND in Mongo: email={doc.get('email')} role={role} _id={doc.get('_id')}")
            else:
                print(f"- NOT FOUND in Mongo: email={em}")

if __name__ == "__main__":
    main()
