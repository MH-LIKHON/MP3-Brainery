# =======================================================
# Step M2: Upsert Topics from Mongo -> SQL (using subject id map)
# =======================================================

import os, json
from pymongo import MongoClient
from sqlalchemy.exc import IntegrityError

from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import Topic

# ------------- Mongo (standalone) -------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/brainery")
_client = MongoClient(MONGO_URI)

def _mongo_db():
    try:
        db = _client.get_default_database()
        if db is not None:
            return db
    except Exception:
        pass
    dbname = MONGO_URI.rsplit("/", 1)[-1].split("?", 1)[0] or "brainery"
    return _client[dbname]

def main():
    # Load subject id map from M1
    map_path = os.path.join("scripts", "_subject_id_map.json")
    if not os.path.exists(map_path):
        print(f"ERROR: subject id map not found at {map_path}. Run M1 first.")
        return

    with open(map_path, "r", encoding="utf-8") as f:
        subj_map = json.load(f)  # {mongo_subject_id(str): sql_subject_id(int)}

    dbm = _mongo_db()
    session = SessionLocal()

    inserted = 0
    updated = 0
    skipped = 0

    try:
        mongo_topics = list(dbm.topics.find({}, {"title":1, "description":1, "subject_id":1}))
        print(f"Found {len(mongo_topics)} Mongo topics.")

        for doc in mongo_topics:
            m_subj = str(doc.get("subject_id") or "")
            title  = (doc.get("title") or "").strip()
            desc   = (doc.get("description") or "") or None

            if not title:
                skipped += 1
                continue

            # Map Mongo subject -> SQL subject_id
            sql_subject_id = subj_map.get(m_subj)
            if not sql_subject_id:
                print(f" ! Skipping topic (no subject map): {title} (mongo subject {m_subj})")
                skipped += 1
                continue

            # Upsert by (subject_id, title)
            row = (
                session.query(Topic)
                       .filter(Topic.subject_id == int(sql_subject_id),
                               Topic.title == title)
                       .one_or_none()
            )

            if row is None:
                row = Topic(subject_id=int(sql_subject_id), title=title, description=desc)
                session.add(row)
                try:
                    session.commit()
                    inserted += 1
                except IntegrityError:
                    session.rollback()
                    # Try to refetch in case of race
                    row = (
                        session.query(Topic)
                               .filter(Topic.subject_id == int(sql_subject_id),
                                       Topic.title == title)
                               .one_or_none()
                    )
                    if row:
                        # Optionally update description if empty
                        if desc and not row.description:
                            row.description = desc
                            session.commit()
                            updated += 1
                    else:
                        skipped += 1
            else:
                # Optional: update description if SQL empty and Mongo has text
                if desc and (not row.description or row.description.strip() == ""):
                    row.description = desc
                    session.commit()
                    updated += 1

        total_sql = session.query(Topic).count()
        print(f"\nSummary: inserted={inserted}, updated={updated}, skipped={skipped}")
        print(f"SQL topics total now: {total_sql}")

    finally:
        session.close()

if __name__ == "__main__":
    main()
