from typing import TYPE_CHECKING

from edict_parser.types.information import Information
from sqlalchemy import Enum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base

if TYPE_CHECKING:
    from wisho.models.entry_element import EntryElement


class ReadingInformation(Base):
    __tablename__ = "reading_info"
    __table_args__ = (UniqueConstraint("element_id", "info", name="uq_reading_info"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    element_id: Mapped[int] = mapped_column(
        ForeignKey("entry_elements.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    info: Mapped[Information] = mapped_column(
        Enum(Information, name="reading_info", native_enum=False),
        nullable=False,
    )

    element: Mapped["EntryElement"] = relationship(back_populates="reading_info")
