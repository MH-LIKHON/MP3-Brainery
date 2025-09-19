# =======================================================
# Step M0: Preview Subjects/Topics in Mongo vs SQL (READ-ONLY)
# =======================================================

from pprint import pprint
import os
from pymongo import MongoClient

from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import Subject, Topic

# -------------------------------------------------------
# Mongo connector (standalone; no Flask app context)
# -------------------------------------------------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/brainery")
_client = MongoClient(MONGO_URI)

def _mongo_db():
    # If URI includes a db, use it; else fall back to 'brainery'
    try:
        db = _client.get_default_database()
        if db is not None:
            return db
    except Exception:
        pass
    dbname = MONGO_URI.rsplit("/", 1)[-1].split("?", 1)[0] or "brainery"
    return _client[dbname]

def preview_mongo():
    print("\n--- Mongo ---")
    db = _mongo_db()
    try:
        m_subj_count = db.subjects.count_documents({})
        m_top_count  = db.topics.count_documents({})
        print(f"subjects: {m_subj_count}")
        print(f"topics  : {m_top_count}")

        print("\nSample Mongo subjects (up to 5):")
        for doc in db.subjects.find({}, {"name":1,"icon":1}).limit(5):
            doc["_id"] = str(doc.get("_id"))
            pprint(doc)

        print("\nSample Mongo topics (up to 5):")
        for doc in db.topics.find({}, {"title":1,"subject_id":1,"description":1}).limit(5):
            doc["_id"] = str(doc.get("_id"))
            sid = doc.get("subject_id")
            doc["subject_id"] = str(sid) if sid else None
            if "description" in doc and doc["description"]:
                txt = doc["description"]
                doc["description"] = (txt[:60] + "") if len(txt) > 60 else txt
            pprint(doc)
    except Exception as e:
        print("Mongo preview error:", e)

def preview_sql():
    print("\n--- SQL ---")
    db = SessionLocal()
    try:
        s_subj_count = db.query(Subject).count()
        s_top_count  = db.query(Topic).count()
        print(f"subjects: {s_subj_count}")
        print(f"topics  : {s_top_count}")

        print("\nSample SQL subjects (up to 5):")
        for s in db.query(Subject).order_by(Subject.name.asc()).limit(5).all():
            print({"id": s.id, "name": s.name, "icon": s.icon})

        print("\nSample SQL topics (up to 5):")
        for t in db.query(Topic).order_by(Topic.created_at.desc()).limit(5).all():
            print({"id": t.id, "subject_id": t.subject_id, "title": t.title})
    finally:
        db.close()

if __name__ == "__main__":
    preview_mongo()
    preview_sql()
