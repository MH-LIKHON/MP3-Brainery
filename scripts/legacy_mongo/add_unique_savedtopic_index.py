from sqlalchemy import text
from brainery_data.sql.db import engine

with engine.begin() as conn:
    conn.execute(
        text("CREATE UNIQUE INDEX IF NOT EXISTS uq_savedtopic_user_title ON saved_topics(user_id, title)")
    )
    rows = conn.execute(text("PRAGMA index_list('saved_topics')")).fetchall()
    print("saved_topics indexes ->", rows)
