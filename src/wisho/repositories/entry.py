from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from wisho.models.entry import Entry
from wisho.models.gloss import Gloss
from wisho.models.kanji import Kanji
from wisho.models.reading import Reading
from wisho.models.sense import Sense


class EntryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def search(self, query: str, limit: int = 20, offset: int = 0) -> list[Entry]:
        stmt = (
            select(Entry)
            .join(Entry.kanji_forms, isouter=True)
            .join(Entry.readings, isouter=True)
            .join(Entry.senses)
            .join(Sense.glosses)
            .where(
                or_(
                    Kanji.text.ilike(f"%{query}%"),
                    Reading.text.ilike(f"%{query}%"),
                    Gloss.text.ilike(f"%{query}%"),
                )
            )
            .options(
                selectinload(Entry.kanji_forms).selectinload(Kanji.priorities),
                selectinload(Entry.readings).selectinload(Reading.priorities),
                selectinload(Entry.senses).selectinload(Sense.glosses),
                selectinload(Entry.senses).selectinload(Sense.pos),
                selectinload(Entry.reading_restrictions),
            )
            .distinct()
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
