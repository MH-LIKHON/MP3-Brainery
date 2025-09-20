# =======================================================
# Step M1: Upsert Subjects from Mongo -> SQL (and write id map)
# =======================================================

import os, json
from pymongo import MongoClient
from sqlalchemy.exc import IntegrityError

from brainery_data.sql.db import SessionLocal
from brainery_data.sql.models import Subject

# -------------------------------------------------------
# Mongo connector (standalone; no Flask app context)
# -------------------------------------------------------
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
    dbm = _mongo_db()
    session = SessionLocal()

    # map: Mongo _id (str) -> SQL subject.id (int)
    id_map = {}

    try:
        mongo_subjects = list(dbm.subjects.find({}, {"name":1, "icon":1}))
        print(f"Found {len(mongo_subjects)} Mongo subjects.")

        for doc in mongo_subjects:
            m_id = str(doc.get("_id"))
            name = (doc.get("name") or "").strip()
            icon = (doc.get("icon") or "") or None
            if not name:
                print(f" - Skipping subject with empty name ({m_id})")
                continue

            # Try to find by exact name (SQL has unique(name))
            row = session.query(Subject).filter(Subject.name == name).one_or_none()

            if row is None:
                # Insert new
                row = Subject(name=name, icon=icon)
                session.add(row)
                try:
                    session.commit()
                    session.refresh(row)
                    print(f" + Inserted: {name} -> id {row.id}")
                except IntegrityError:
                    # someone else inserted with same name; recover
                    session.rollback()
                    row = session.query(Subject).filter(Subject.name == name).one_or_none()
                    if row:
                        print(f" = Exists after race: {name} -> id {row.id}")
                    else:
                        print(f" ! Failed to insert: {name}")
                        continue
            else:
                # Update icon if changed (optional)
                if icon and row.icon != icon:
                    row.icon = icon
                    session.commit()
                    print(f" ~ Updated icon: {name} -> {icon}")

            id_map[m_id] = int(row.id)

        # Write mapping so topics step can resolve subject_id
        os.makedirs("scripts", exist_ok=True)
        map_path = os.path.join("scripts", "_subject_id_map.json")
        with open(map_path, "w", encoding="utf-8") as f:
            json.dump(id_map, f, ensure_ascii=False, indent=2)
        print(f"\nWrote subject id map -> {map_path} ({len(id_map)} entries)")

        # Show resulting SQL counts
        total_sql = session.query(Subject).count()
        print(f"Subjects in SQL after upsert: {total_sql}")

    finally:
        session.close()

if __name__ == "__main__":
    main()
