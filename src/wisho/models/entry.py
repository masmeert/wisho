from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base
from wisho.models.kanji import Kanji
from wisho.models.reading import Reading
from wisho.models.reading_restriction import ReadingRestriction
from wisho.models.sense import Sense


class Entry(Base):
    """Represents a JMdict entry `<entry>`

    Attributes:
        id:
            Primary key, the JMdict sequence number. Mapped from `<ent_seq>`.
        kanji_forms:
            All kanji spellings for this entry. From `<k_ele>/<keb>`.
        readings:
            All kana readings for this entry. From `<r_ele>/<reb>`.
        senses:
            Ordered list of senses (meanings). From `<sense>`.
        reading_restrictions:
            Optional valid pairs for `Reading` <-> `Kanji`. From `<re_restr>`.
    """

    __tablename__ = "entry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    kanji_forms: Mapped[list[Kanji]] = relationship(back_populates="entry", cascade="all, delete-orphan")
    readings: Mapped[list[Reading]] = relationship(back_populates="entry", cascade="all, delete-orphan")
    senses: Mapped[list[Sense]] = relationship(back_populates="entry", cascade="all, delete-orphan")
    reading_restrictions: Mapped[list[ReadingRestriction]] = relationship(
        back_populates="entry", cascade="all, delete-orphan"
    )
