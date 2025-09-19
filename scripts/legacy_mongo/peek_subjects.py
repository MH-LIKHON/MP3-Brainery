from sqlalchemy import select
from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import Subject

db = SessionLocal()
try:
    count = db.query(Subject).count()
    print("Subjects count ->", count)
    for s in db.execute(select(Subject).order_by(Subject.name.asc()).limit(10)).scalars().all():
        print("  Subject:", s.id, s.name, s.icon)
finally:
    db.close()
