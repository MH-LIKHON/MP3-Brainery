from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import SavedTopic
db = SessionLocal()
try:
    rows = db.query(SavedTopic).order_by(SavedTopic.created_at.desc()).all()
    print(f"Saved topics -> {len(rows)}")
    for r in rows:
        print(r.id, r.user_id, r.title, r.created_at)
finally:
    db.close()
