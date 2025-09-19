from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import UserSQL
from werkzeug.security import generate_password_hash, check_password_hash

EMAIL = "30m.l@live.co.uk"
NEW_PW = "Qwerty@12345"

db = SessionLocal()
try:
    u = db.query(UserSQL).filter(UserSQL.email == EMAIL).one_or_none()
    if not u:
        print("SQL user not found:", EMAIL)
    else:
        u.password = generate_password_hash(NEW_PW)  # pbkdf2:sha256
        db.commit()
        # verify
        ok = check_password_hash(u.password or "", NEW_PW)
        print(f"Updated {EMAIL}. Hash starts with: {(u.password or '')[:20]}  matches_test={ok}")
finally:
    db.close()
