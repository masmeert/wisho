from sqlite3 import IntegrityError

from sqlalchemy.orm import Session

from wisho.db.engine import get_engine
from wisho.db.jmdict import (
    Base,
    Entry,
    EntryPriority,
    Gloss,
    Kanji,
    Reading,
    ReadingRestriction,
    Sense,
    SensePOS,
)
from wisho.db.seed import add_entry_to_db
from wisho.jmdict.parser import parse_jmdict_file

__all__ = [
    "Entry",
    "EntryPriority",
    "Gloss",
    "Kanji",
    "Reading",
    "ReadingRestriction",
    "Sense",
    "SensePOS",
]


if __name__ == "__main__":
    # Seed database with jmdict entries
    engine = get_engine()
    Base.metadata.create_all(engine)

    entries = parse_jmdict_file()
    with Session(engine) as session:
        for entry in entries:
            try:
                add_entry_to_db(session, entry)
            except IntegrityError:
                session.rollback()
                continue
        session.commit()
