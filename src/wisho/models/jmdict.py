from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wisho.core.db.base import Base


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kanjis: Mapped[list["Kanji"]] = relationship(back_populates="word", cascade="all, delete-orphan")
    readings: Mapped[list["Reading"]] = relationship(back_populates="word", cascade="all, delete-orphan")
    senses: Mapped[list["Sense"]] = relationship(back_populates="word", cascade="all, delete-orphan")


class Kanji(Base):
    __tablename__ = "kanjis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    word_id: Mapped[int] = mapped_column(Integer, ForeignKey("words.id"), index=True)
    text: Mapped[str] = mapped_column(String, index=True)
    is_common: Mapped[bool] = mapped_column(Boolean)
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    word: Mapped["Word"] = relationship(back_populates="kanjis")


class Reading(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    word_id: Mapped[int] = mapped_column(Integer, ForeignKey("words.id"), index=True)
    text: Mapped[str] = mapped_column(String, index=True)
    is_common: Mapped[bool] = mapped_column(Boolean)
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    applies_to_kanji: Mapped[list[str]] = mapped_column(JSONB, default=list)
    word: Mapped["Word"] = relationship(back_populates="readings")


class Sense(Base):
    __tablename__ = "senses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    word_id: Mapped[int] = mapped_column(Integer, ForeignKey("words.id"), index=True)
    part_of_speech: Mapped[list[str]] = mapped_column(JSONB, default=list)
    applies_to_kanji: Mapped[list[str]] = mapped_column(JSONB, default=list)
    applies_to_reading: Mapped[list[str]] = mapped_column(JSONB, default=list)
    fields: Mapped[list[str]] = mapped_column(JSONB, default=list)
    dialects: Mapped[list[str]] = mapped_column(JSONB, default=list)
    misc: Mapped[list[str]] = mapped_column(JSONB, default=list)
    infos: Mapped[list[str]] = mapped_column(JSONB, default=list)
    word: Mapped["Word"] = relationship(back_populates="senses")
    examples: Mapped[list["SenseExample"]] = relationship(back_populates="sense", cascade="all, delete-orphan")
    glosses: Mapped[list["Gloss"]] = relationship(back_populates="sense", cascade="all, delete-orphan")


class SenseExample(Base):
    __tablename__ = "sense_examples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sense_id: Mapped[int] = mapped_column(Integer, ForeignKey("senses.id"), index=True)
    source: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    jpn: Mapped[str] = mapped_column(String)
    eng: Mapped[str] = mapped_column(String)
    sense: Mapped["Sense"] = relationship(back_populates="examples")


class Gloss(Base):
    __tablename__ = "glosses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sense_id: Mapped[int] = mapped_column(Integer, ForeignKey("senses.id"), index=True)
    type: Mapped[str | None] = mapped_column(String, nullable=True)
    text: Mapped[str] = mapped_column(String)
    sense: Mapped["Sense"] = relationship(back_populates="glosses")
