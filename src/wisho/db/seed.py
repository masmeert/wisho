from sqlalchemy.orm import Session

from wisho.db.jmdict import Entry, EntryPriority, Gloss, Kanji, Reading, ReadingRestriction, Sense, SensePOS
from wisho.jmdict.dto import EntryDTO


def add_kanji_forms_to_db(session: Session, entry: EntryDTO) -> dict[str, Kanji]:
    records_map = {}
    for kanji in entry.kanji_forms:
        kanji_record = Kanji(
            entry_id=entry.id,
            text=kanji.text,
        )
        session.add(kanji_record)
        session.flush()
        records_map[kanji.text] = kanji_record
        for raw_priority in kanji.priorities:
            priority_record = EntryPriority(
                entry_id=entry.id,
                kanji_id=kanji_record.id,
                raw=raw_priority,
            )
            session.add(priority_record)
    return records_map


def add_readings_to_db(session: Session, entry: EntryDTO, kanji_map: dict[str, Kanji]) -> None:
    for reading in entry.readings:
        reading_record = Reading(
            entry_id=entry.id,
            text=reading.text,
            no_kanji=reading.no_kanji,
        )

        session.add(reading_record)
        session.flush()

        for raw_priority in reading.priorities:
            priority_record = EntryPriority(
                entry_id=entry.id,
                reading_id=reading_record.id,
                raw=raw_priority,
            )
            session.add(priority_record)

        for kanji_text in reading.restrictions:
            if kanji_text in kanji_map:
                session.add(
                    ReadingRestriction(
                        entry_id=entry.id,
                        reading_id=reading_record.id,
                        kanji_id=kanji_map[kanji_text].id,
                    )
                )


def add_senses_to_db(session: Session, entry: EntryDTO) -> None:
    for sense_index, sense in enumerate(entry.senses, start=1):
        sense_record = Sense(
            entry_id=entry.id,
            order=sense_index,
        )
        session.add(sense_record)
        session.flush()

        for tag in sense.pos:
            part_of_speech = SensePOS(sense_id=sense_record.id, tag=tag)
            session.add(part_of_speech)

        for gloss_index, gloss in enumerate(sense.glosses, start=1):
            gloss_record = Gloss(
                sense_id=sense_record.id,
                order=gloss_index,
                text=gloss.text,
                lang=gloss.lang,
            )
            session.add(gloss_record)


def add_entry_to_db(session: Session, entry: EntryDTO) -> None:
    exists = session.get(Entry, entry.id)
    if exists:
        return

    entry_record = Entry(id=entry.id)
    session.add(entry_record)
    session.flush()

    kanji_map = add_kanji_forms_to_db(session, entry)
    add_readings_to_db(session, entry, kanji_map)
    add_senses_to_db(session, entry)
