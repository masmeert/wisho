from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base

if TYPE_CHECKING:
    from wisho.models.kanji import Kanji
    from wisho.models.reading import Reading


class EntryPriority(Base):
    """Represents a frequency tag attached to a kanji or reading.

    JMdict uses `<ke_pri>` (kanji) and `<re_pri>` (reading). We store both in one table:
      - If the tag belongs to a kanji form: `kanji_id` is set (and `reading_id` is NULL).
      - If the tag belongs to a reading form: `reading_id` is set (and `kanji_id` is NULL).

    Attributes:
        id:
            Primary key.
        entry_id:
            Foreign key to `Entry`.
        kanji_id:
            Foreign key to `Kanji` when this priority is for a kanji form; NULL otherwise.
        reading_id:
            Foreign key to `Reading` when this priority is for a reading form; NULL otherwise.
        raw:
            The original priority token (e.g., 'nf14', 'news1', 'ichi1').

        kanji:
            Relationship back to the `Kanji` (if `kanji_id` is set).
        reading:
            Relationship back to the `Reading` (if `reading_id` is set).
    """

    __tablename__ = "entry_priority"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entry.id"), nullable=False, index=True)
    kanji_id: Mapped[int | None] = mapped_column(ForeignKey("kanji.id"), index=True)
    reading_id: Mapped[int | None] = mapped_column(ForeignKey("reading.id"), index=True)
    raw: Mapped[str] = mapped_column(String, nullable=False)

    kanji: Mapped[Kanji | None] = relationship(back_populates="priorities")
    reading: Mapped[Reading | None] = relationship(back_populates="priorities")

    __table_args__ = (
        # Exactly one target must be set (XOR)
        CheckConstraint(
            "(kanji_id IS NOT NULL) <> (reading_id IS NOT NULL)",
            name="ck_priority_exclusive_target",
        ),
        # Avoid duplicates on either side
        UniqueConstraint("kanji_id", "raw", name="uix_priority_kanji_raw"),
        UniqueConstraint("reading_id", "raw", name="uix_priority_reading_raw"),
        Index("ix_priority_raw", "raw"),
    )
