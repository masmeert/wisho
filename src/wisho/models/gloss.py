from typing import TYPE_CHECKING

from edict_parser.types.gloss import GlossType
from edict_parser.types.language import Language
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base

if TYPE_CHECKING:
    from wisho.models.sense import Sense


class Gloss(Base):
    __tablename__ = "glosses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sense_id: Mapped[int] = mapped_column(ForeignKey("senses.id", ondelete="CASCADE"), index=True, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    language: Mapped[Language] = mapped_column(Enum(Language, native_enum=False), nullable=False)
    gloss_type: Mapped[GlossType] = mapped_column(Enum(GlossType, native_enum=False), nullable=True)

    Sense: Mapped["Sense"] = relationship("Sense", back_populates="Glosses")
