from typing import TYPE_CHECKING

from edict_parser.types.priority import PriorityType
from sqlalchemy import Enum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base

if TYPE_CHECKING:
    from wisho.models.entry_element import EntryElement


class ElementPriority(Base):
    """
    Mirrors pydantic Priority (priority_type, level) for an EntryElement.
    """

    __tablename__ = "element_priorities"
    __table_args__ = (UniqueConstraint("element_id", "priority_type", "level", name="uq_element_priority"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    element_id: Mapped[int] = mapped_column(
        ForeignKey("entry_elements.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    priority_type: Mapped[PriorityType] = mapped_column(
        Enum(PriorityType, name="priority_type", native_enum=False),
        nullable=False,
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False)

    element: Mapped["EntryElement"] = relationship(back_populates="priorities")
