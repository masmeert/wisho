from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base

if TYPE_CHECKING:
    from wisho.models.entry import Entry


class ReadingRestriction(Base):
    """Represents a VALID reading-kanji pairing for an entry `<re_restr>`.

    Attributes:
        id:
            Primary key.
        entry_id:
            Foreign key to `Entry`.
        reading_id:
            Foreign key to the `Reading`.
        kanji_id:
            Foreign key to the `Kanji`.

        entry:
            Relationship back to the parent `Entry`.
    """

    __tablename__ = "reading_restriction"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entry.id"), nullable=False, index=True)
    reading_id: Mapped[int] = mapped_column(ForeignKey("reading.id"), nullable=False, index=True)
    kanji_id: Mapped[int] = mapped_column(ForeignKey("kanji.id"), nullable=False, index=True)

    entry: Mapped[Entry] = relationship(back_populates="reading_restrictions")

    __table_args__ = (UniqueConstraint("entry_id", "reading_id", "kanji_id", name="uix_rrestr_unique"),)
