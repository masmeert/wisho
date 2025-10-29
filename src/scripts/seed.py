# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "edict-parser",
#     "sqlalchemy",
#     "wisho",
# ]
# ///

import asyncio
from collections.abc import Sequence

from edict_parser.jmdict.parsing import parse_jmdict_file
from edict_parser.schemas.entry import Entry as EntryDTO
from sqlalchemy.ext.asyncio import AsyncSession

from wisho.core.db.session import get_async_session
from wisho.models.entry import Entry
from wisho.models.entry_priority import EntryPriority
from wisho.models.gloss import Gloss
from wisho.models.kanji import Kanji
from wisho.models.reading import Reading
from wisho.models.sense import Sense
from wisho.models.sense_pos import SensePOS


async def add_kanji_forms_to_db(session: AsyncSession, entry: EntryDTO) -> None:
    # Filter elements to get only kanji forms
    kanji_elements = [element for element in entry.elements if element.is_kanji]

    for kanji in kanji_elements:
        # Convert reading_info enums to comma-separated string
        reading_info_str = ",".join([info.value for info in kanji.reading_info]) if kanji.reading_info else None

        kanji_record = Kanji(
            entry_id=entry.sequence,
            text=kanji.text,
            reading_info=reading_info_str,
        )
        session.add(kanji_record)
        await session.flush()
        for priority in kanji.priorities:
            priority_record = EntryPriority(
                entry_id=entry.sequence,
                kanji_id=kanji_record.id,
                raw=f"{priority.priority_type.value}{priority.level:02d}",
            )
            session.add(priority_record)


async def add_readings_to_db(session: AsyncSession, entry: EntryDTO) -> None:
    # Filter elements to get only reading forms
    reading_elements = [element for element in entry.elements if not element.is_kanji]

    for reading in reading_elements:
        # Convert reading_info enums to comma-separated string
        reading_info_str = ",".join([info.value for info in reading.reading_info]) if reading.reading_info else None

        reading_record = Reading(
            entry_id=entry.sequence,
            text=reading.text,
            no_kanji=reading.no_true_reading,
            reading_info=reading_info_str,
        )
        session.add(reading_record)
        await session.flush()

        for priority in reading.priorities:
            priority_record = EntryPriority(
                entry_id=entry.sequence,
                reading_id=reading_record.id,
                raw=f"{priority.priority_type.value}{priority.level:02d}",
            )
            session.add(priority_record)

        # Note: Reading restrictions are not currently handled in the new schema structure
        # This would need to be implemented based on how the parser handles re_restr elements


async def add_senses_to_db(session: AsyncSession, entry: EntryDTO) -> None:
    for sense_index, sense in enumerate(entry.senses, start=1):
        sense_record = Sense(
            entry_id=entry.sequence,
            order=sense_index,
            misc=sense.misc.value if sense.misc else None,
            field=sense.field.value if sense.field else None,
            dialect=sense.dialect.value if sense.dialect else None,
            antonym=sense.antonym,
            xref=sense.xref,
            information=sense.information,
            gairaigo=sense.gairaigo.value if sense.gairaigo else None,
        )
        session.add(sense_record)
        await session.flush()

        for tag in sense.part_of_speech:
            part_of_speech = SensePOS(sense_id=sense_record.id, tag=tag.value)
            session.add(part_of_speech)

        for gloss_index, gloss in enumerate(sense.glosses, start=1):
            gloss_record = Gloss(
                sense_id=sense_record.id,
                order=gloss_index,
                text=gloss.text,
                lang=gloss.language.value,
                gtype=gloss.gtype.value if gloss.gtype else None,
            )
            session.add(gloss_record)


async def add_entry_to_db(session: AsyncSession, entry: EntryDTO) -> None:
    exists = await session.get(Entry, entry.sequence)
    if exists:
        return

    entry_record = Entry(id=entry.sequence)
    session.add(entry_record)
    await session.flush()
    await add_kanji_forms_to_db(session, entry)
    await add_readings_to_db(session, entry)
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
