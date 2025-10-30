from typing import TYPE_CHECKING

from edict_parser.types.dialect import Dialect
from edict_parser.types.field import SubjectField
from edict_parser.types.information import MiscellaneousInformation
from edict_parser.types.language import Gairaigo
from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base

if TYPE_CHECKING:
    from wisho.models.entry import Entry
    from wisho.models.gloss import Gloss
    from wisho.models.part_of_speech import PartOfSpeech


class Sense(Base):
    __tablename__ = "senses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entry_sequence: Mapped[int] = mapped_column(
        ForeignKey("entries.sequence", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    sense_index: Mapped[int | None] = mapped_column(Integer, nullable=True)

    misc: Mapped[MiscellaneousInformation | None] = mapped_column(
        Enum(MiscellaneousInformation, name="misc_info", native_enum=False),
        nullable=True,
    )
    field: Mapped[SubjectField | None] = mapped_column(
        Enum(SubjectField, name="subject_field", native_enum=False),
        nullable=True,
    )
    dialect: Mapped[Dialect | None] = mapped_column(
        Enum(Dialect, name="dialect", native_enum=False),
        nullable=True,
    )
    gairaigo: Mapped[Gairaigo | None] = mapped_column(
        Enum(Gairaigo, name="gairaigo", native_enum=False),
        nullable=True,
    )

    antonym: Mapped[str | None] = mapped_column(String, nullable=True)
    xref: Mapped[str | None] = mapped_column(String, nullable=True)
    information: Mapped[str | None] = mapped_column(String, nullable=True)

    entry: Mapped["Entry"] = relationship(back_populates="senses")

    glosses: Mapped[list["Gloss"]] = relationship(
        back_populates="sense",
        cascade="all, delete-orphan",
        order_by="Gloss.id",
    )

    parts_of_speech: Mapped[list["PartOfSpeech"]] = relationship(
        back_populates="sense",
        cascade="all, delete-orphan",
        order_by="PartOfSpeech.id",
    )
