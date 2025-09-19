from sqlalchemy import inspect, text
from brainery_data.sql.db import engine
from brainery_data.sql.models import Base

# create any missing tables (this will create saved_topics)
Base.metadata.create_all(engine)

# show tables and saved_topics indexes (unique should be 1)
insp = inspect(engine)
print("Tables now:", insp.get_table_names())
with engine.begin() as conn:
    idx = conn.execute(text("PRAGMA index_list('saved_topics')")).fetchall()
    print("saved_topics indexes:", idx)
