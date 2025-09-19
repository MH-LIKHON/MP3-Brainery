from brainery_data.sql.db import SessionLocal, engine
from brainery_data.sql.models import Subject, Topic, UserSQL
from sqlalchemy import inspect

def main():
    print("DB URL:", engine.url)
    insp = inspect(engine)
    print("Tables:", insp.get_table_names())

    db = SessionLocal()
    try:
        subjects = db.query(Subject).count()
        topics = db.query(Topic).count()
        users = db.query(UserSQL).count()
        print(f"Counts -> subjects={subjects}, topics={topics}, users={users}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
