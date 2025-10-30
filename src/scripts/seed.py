# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "edict",
#     "sqlalchemy",
#     "wisho",
# ]
# ///
import asyncio
from pathlib import Path

from edict.core.helpers import load_json_file
from edict.schemas.jmdict import Word as WordDTO
from sqlalchemy import select

from wisho.core.db.session import local_session
from wisho.models.jmdict import Gloss, Kanji, Reading, Sense, SenseExample, Word

DICTIONARY_FILE_PATH = Path(__file__).resolve().parents[2] / "packages" / "edict" / "resources" / "jmdict.json"


def pydantic_to_sqlalchemy(edict_word: WordDTO) -> Word:
    word = Word(id=edict_word.id)

    for kanji in edict_word.kanjis:
        word.kanjis.append(
            Kanji(
                text=kanji.text,
                is_common=kanji.is_common,
                tags=kanji.tags,
            )
        )

    for reading in edict_word.readings:
        word.readings.append(
            Reading(
                text=reading.text,
                is_common=reading.is_common,
                tags=reading.tags,
                applies_to_kanji=reading.applies_to_kanji,
            )
        )

    for sense in edict_word.senses:
        db_sense = Sense(
            part_of_speech=[pos.value for pos in sense.part_of_speech],
            applies_to_kanji=sense.applies_to_kanji,
            applies_to_reading=sense.applies_to_reading,
            fields=[field.value for field in sense.fields],
            dialects=[dialect.value for dialect in sense.dialects],
            misc=[misc.value for misc in sense.misc],
            infos=sense.infos,
        )

        for gloss in sense.glosses:
            db_sense.glosses.append(
                Gloss(
                    type=gloss.type.value if gloss.type else None,
                    text=gloss.text,
                )
            )

        for example in sense.examples:
            db_sense.examples.append(
                SenseExample(
                    source=example.source,
                    text=example.text,
                    jpn=example.jpn,
                    eng=example.eng,
                )
            )

        word.senses.append(db_sense)

    return word


async def seed_database(batch_size: int = 1000) -> None:
    jmdict_data = load_json_file(DICTIONARY_FILE_PATH)
    json_words = jmdict_data["words"]

    print(f"Loaded {len(json_words)} word entries")

    async with local_session() as session:
        result = await session.execute(select(Word).limit(1))
        existing_word = result.scalar_one_or_none()

        if existing_word:
            print("Database already contains data. Skipping seed.")
            return

        print("Converting and inserting entries...")
        words_to_insert = []

        for i, word_json in enumerate(json_words):
            edict_word = WordDTO.from_json(word_json)

            db_word = pydantic_to_sqlalchemy(edict_word)
            words_to_insert.append(db_word)

            if len(words_to_insert) >= batch_size:
                session.add_all(words_to_insert)
                await session.flush()
                print(f"Inserted {i + 1}/{len(json_words)} entries...")
                words_to_insert = []

        if words_to_insert:
            session.add_all(words_to_insert)
            await session.flush()

        await session.commit()
        print(f"Successfully seeded database with {len(json_words)} words!")


if __name__ == "__main__":
    asyncio.run(seed_database())
