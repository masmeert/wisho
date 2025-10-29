from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base
from wisho.models.entry import Entry
from wisho.models.gloss import Gloss
from wisho.models.sense_pos import SensePOS


class Sense(Base):
    """Represents one sense (meaning) block of an entry `<sense>`.

    Attributes:
    id:
        Primary key.
    entry_id:
        Foreign key to `Entry`.
    order:
        1-based position of the sense within the entry. From the order of `<sense>`.

    entry:
        Relationship back to the parent `Entry`.
    glosses:
        The list of glosses (translations/definitions) for this sense. From `<gloss>`.
    pos:
        The list of part-of-speech tags for this sense. From `<pos>`.
    """

    __tablename__ = "sense"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entry.id"), nullable=False, index=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-based

    entry: Mapped[Entry] = relationship(back_populates="senses")
    glosses: Mapped[list[Gloss]] = relationship(back_populates="sense", cascade="all, delete-orphan")
    pos: Mapped[list[SensePOS]] = relationship(back_populates="sense", cascade="all, delete-orphan")
