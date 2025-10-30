from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base

if TYPE_CHECKING:
    from wisho.models.entry import Entry
    from wisho.models.priority import ElementPriority
    from wisho.models.reading_information import ReadingInformation


class EntryElement(Base):
    __tablename__ = "entry_elements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entry_sequence: Mapped[int] = mapped_column(
        ForeignKey("entries.sequence", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    text: Mapped[str] = mapped_column(String, nullable=False)
    is_kanji: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    no_true_reading: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    entry: Mapped["Entry"] = relationship(back_populates="elements")

    priorities: Mapped[list["ElementPriority"]] = relationship(
        back_populates="element",
        cascade="all, delete-orphan",
        order_by="ElementPriority.id",
    )

    reading_info: Mapped[list["ReadingInformation"]] = relationship(
        back_populates="element",
        cascade="all, delete-orphan",
        order_by="ElementReadingInfo.id",
    )
