from sqlalchemy import inspect
from brainery_data.sql.db import engine, SessionLocal
from brainery_data.sql.models import UserSQL

print("Engine URL ->", engine.url)

insp = inspect(engine)
print("Tables ->", insp.get_table_names())

with SessionLocal() as s:
    total = s.query(UserSQL).count()
    first = s.query(UserSQL).order_by(UserSQL.id.asc()).first()
    print("User count ->", total)
    if first:
        print("First user ->", first.id, first.email, first.role if hasattr(first, "role") else None)
