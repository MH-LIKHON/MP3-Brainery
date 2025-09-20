from brainery_data.sql.db import engine, SessionLocal
from brainery_data.sql.models import Base, UserSQL

# 1) Create tables if they do not exist
Base.metadata.create_all(bind=engine)

# 2) Show current SQL users
session = SessionLocal()
try:
    users = session.query(UserSQL).order_by(UserSQL.id.desc()).limit(5).all()
    print("Latest SQL users (up to 5):")
    for u in users:
        print(f"- id={u.id}, email={u.email}, username={u.username}, role={u.role}, created_at={u.created_at}")
finally:
    session.close()
