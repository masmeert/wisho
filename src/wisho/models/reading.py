from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base

if TYPE_CHECKING:
    from wisho.models.entry import Entry
    from wisho.models.entry_priority import EntryPriority


class Reading(Base):
    """Represents a reading (kana) of the entry `<r_ele>/<reb>`.

    Attributes:
        id:
            Primary key.
        entry_id:
            Foreign key to `Entry.id` (JMdict `<ent_seq>`).
        text:
            The reading in kana. From `<r_ele>/<reb>`.
        no_kanji:
            Whether the reading has no associated kanji form. True if `<re_nokanji/>` present.

        entry:
            Relationship back to the parent `Entry`.
        priorities:
            List of frequency tags attached to this reading form. From `<re_pri>`.
    """

    __tablename__ = "reading"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entry.id"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    no_kanji: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    entry: Mapped[Entry] = relationship(back_populates="readings")
    priorities: Mapped[list[EntryPriority]] = relationship(back_populates="reading", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("entry_id", "text", name="uix_reading_entry_text"),
        Index("ix_reading_text", "text"),
    )
