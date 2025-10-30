from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base

if TYPE_CHECKING:
    from wisho.models.entry_element import EntryElement
    from wisho.models.sense import Sense


class Entry(Base):
    __tablename__ = "entries"

    # In JMdict, "sequence" is globally unique; use it as the PK
    sequence: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_common: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # children
    elements: Mapped[list["EntryElement"]] = relationship(
        back_populates="entry",
        cascade="all, delete-orphan",
        order_by="EntryElement.id",
    )
    senses: Mapped[list["Sense"]] = relationship(
        back_populates="entry",
        cascade="all, delete-orphan",
        order_by="Sense.id",
    )
