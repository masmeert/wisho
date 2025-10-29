# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "jmdict-parser",
#     "sqlalchemy",
#     "wisho",
# ]
# ///

import asyncio
from collections.abc import Sequence

from jmdict_parser.parsing import parse_jmdict_file
from jmdict_parser.schemas.entry import Entry as EntryDTO
from sqlalchemy.ext.asyncio import AsyncSession

from wisho.core.db.session import get_async_session
from wisho.models.entry import Entry
from wisho.models.entry_priority import EntryPriority
from wisho.models.gloss import Gloss
from wisho.models.kanji import Kanji
from wisho.models.reading import Reading
from wisho.models.reading_restriction import ReadingRestriction
from wisho.models.sense import Sense
from wisho.models.sense_pos import SensePOS


async def add_kanji_forms_to_db(session: AsyncSession, entry: EntryDTO) -> dict[str, Kanji]:
    records_map = {}
    for kanji in entry.kanji_forms:
        kanji_record = Kanji(
            entry_id=entry.id,
            text=kanji.text,
        )
        session.add(kanji_record)
        await session.flush()
        records_map[kanji.text] = kanji_record
        for raw_priority in kanji.priorities:
            priority_record = EntryPriority(
                entry_id=entry.id,
                kanji_id=kanji_record.id,
                raw=raw_priority,
            )
            session.add(priority_record)
    return records_map


async def add_readings_to_db(session: AsyncSession, entry: EntryDTO, kanji_map: dict[str, Kanji]) -> None:
    for reading in entry.readings:
        reading_record = Reading(
            entry_id=entry.id,
            text=reading.text,
            no_kanji=reading.no_kanji,
        )
        session.add(reading_record)
        await session.flush()

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


async def add_senses_to_db(session: AsyncSession, entry: EntryDTO) -> None:
    for sense_index, sense in enumerate(entry.senses, start=1):
        sense_record = Sense(
            entry_id=entry.id,
            order=sense_index,
        )
        session.add(sense_record)
        await session.flush()

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


async def add_entry_to_db(session: AsyncSession, entry: EntryDTO) -> None:
    exists = await session.get(Entry, entry.id)
    if exists:
        return

    entry_record = Entry(id=entry.id)
    session.add(entry_record)
    await session.flush()
    kanji_map = await add_kanji_forms_to_db(session, entry)
    await add_readings_to_db(session, entry, kanji_map)
    await add_senses_to_db(session, entry)


async def seed_entries(session: AsyncSession, entries: Sequence[EntryDTO]) -> None:
    for entry in entries:
        try:
            await add_entry_to_db(session, entry)
        except Exception:
            await session.rollback()
            raise
        else:
            await session.commit()


async def main() -> None:
    entries = parse_jmdict_file()
    async for session in get_async_session():
        await seed_entries(session, entries)
        break


if __name__ == "__main__":
    asyncio.run(main())
