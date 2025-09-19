# =======================================================
# Step V1: Verify topics per subject (SQL)
# =======================================================

from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import Subject, Topic

db = SessionLocal()
try:
    for s in db.query(Subject).order_by(Subject.id.asc()).all():
        count = db.query(Topic).filter(Topic.subject_id == s.id).count()
        print(f"{s.id:>2}  {s.name}  -> {count} topics")
finally:
    db.close()
