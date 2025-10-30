from typing import TYPE_CHECKING

from edict_parser.types.part_of_speech import PartOfSpeech as PartOfSpeechEnum
from sqlalchemy import Enum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base

if TYPE_CHECKING:
    from wisho.models.sense import Sense


class PartOfSpeech(Base):
    __tablename__ = "sense_parts_of_speech"
    __table_args__ = (UniqueConstraint("sense_id", "pos", name="uq_sense_pos"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sense_id: Mapped[int] = mapped_column(
        ForeignKey("senses.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    pos: Mapped[PartOfSpeechEnum] = mapped_column(
        Enum(PartOfSpeechEnum, name="part_of_speech", native_enum=False),
        nullable=False,
    )

    sense: Mapped["Sense"] = relationship(back_populates="parts_of_speech")
