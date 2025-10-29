from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base

if TYPE_CHECKING:
    from wisho.models.sense import Sense


class Gloss(Base):
    """Represents a gloss inside a sense `<gloss>`.

    Attributes:
        id:
            Primary key.
        sense_id:
            Foreign key to the Sense it belongs to.
        order:
            1-based position of the gloss within the sense.
        text:
            The gloss text (definition). From the content of `<gloss>`.
        lang:
            Language of the gloss (g_lang). Defaults to 'eng' in JMdict_e.

        sense:
            Relationship back to the parent `Sense`.
    """

    __tablename__ = "gloss"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sense_id: Mapped[int] = mapped_column(ForeignKey("sense.id"), nullable=False, index=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    lang: Mapped[str] = mapped_column(String, nullable=False, default="eng")

    sense: Mapped[Sense] = relationship(back_populates="glosses")

    __table_args__ = (Index("ix_gloss_text", "text"),)
