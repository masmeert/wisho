from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base

if TYPE_CHECKING:
    from wisho.models.entry import Entry
    from wisho.models.entry_priority import EntryPriority


class Kanji(Base):
    """Represents a kanji written form of the entry `<k_ele>/<keb>`.

    Attributes:
        id:
            Primary key.
        entry_id:
            Foreign key to `Entry`.
        text:
            The kanji spelling of the word. From `<k_ele>/<keb>`.

        entry:
            Relationship back to the parent `Entry`.
        priorities:
            List of frequency tags attached to this kanji form. From `<ke_pri>`.
    """

    __tablename__ = "kanji"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entry.id"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)

    entry: Mapped[Entry] = relationship(back_populates="kanji_forms")
    priorities: Mapped[list[EntryPriority]] = relationship(back_populates="kanji", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("entry_id", "text", name="uix_kanji_entry_text"),
        Index("ix_kanji_text", "text"),
    )
