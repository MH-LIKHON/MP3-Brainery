from sqlalchemy import text
from brainery_data.sql.db import engine

with engine.begin() as conn:
    rows = conn.execute(text("""
        SELECT user_id, title, COUNT(*) AS c
        FROM saved_topics
        GROUP BY user_id, title
        HAVING COUNT(*) > 1
    """)).fetchall()

if not rows:
    print(" No duplicates found. Safe to add unique index.")
else:
    print(" Duplicates found (user_id, title, count):")
    for r in rows:
        print(tuple(r))
