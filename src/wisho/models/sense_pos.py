from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base
from wisho.models.sense import Sense


class SensePOS(Base):
    """Represents a part-of-speech tag for a sense `<pos>`.

    Attributes:
        id:
            Primary key.
        sense_id:
            Foreign key to the `Sense` it belongs to.
        tag:
            The part-of-speech tag value. From `<pos>` (e.g., 'n', 'v1', 'adj-i').

        sense:
            Relationship back to the parent `Sense`.
    """

    __tablename__ = "sense_pos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sense_id: Mapped[int] = mapped_column(ForeignKey("sense.id"), nullable=False, index=True)
    tag: Mapped[str] = mapped_column(String, nullable=False)

    sense: Mapped[Sense] = relationship(back_populates="pos")

    __table_args__ = (UniqueConstraint("sense_id", "tag", name="uix_sense_pos_once"),)
