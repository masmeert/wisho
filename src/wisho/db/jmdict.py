from typing import Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


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

    kanji_forms: Mapped[list["Kanji"]] = relationship(back_populates="entry", cascade="all, delete-orphan")
    readings: Mapped[list["Reading"]] = relationship(back_populates="entry", cascade="all, delete-orphan")
    senses: Mapped[list["Sense"]] = relationship(back_populates="entry", cascade="all, delete-orphan")
    reading_restrictions: Mapped[list["ReadingRestriction"]] = relationship(
        back_populates="entry", cascade="all, delete-orphan"
    )


class Kanji(Base):
    """Represents a kanji written form of the entry `<k_ele>/<keb>`.

    Attributes:
        id:
            Primary key.
        entry_id:
            Foreign key to `Entry`.
        text:
            The kanji spelling of the word. From `<k_ele>/<keb>`.

        entry:
            Relationship back to the parent `Entry`.
        priorities:
            List of frequency tags attached to this kanji form. From `<ke_pri>`.
    """

    __tablename__ = "kanji"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entry.id"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)

    entry: Mapped["Entry"] = relationship(back_populates="kanji_forms")
    priorities: Mapped[list["EntryPriority"]] = relationship(back_populates="kanji", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("entry_id", "text", name="uix_kanji_entry_text"),
        Index("ix_kanji_text", "text"),
    )


class Reading(Base):
    """Represents a reading (kana) of the entry `<r_ele>/<reb>`.

    Attributes:
        id:
            Primary key.
        entry_id:
            Foreign key to `Entry.id` (JMdict `<ent_seq>`).
        text:
            The reading in kana. From `<r_ele>/<reb>`.
        no_kanji:
            Whether the reading has no associated kanji form. True if `<re_nokanji/>` present.

        entry:
            Relationship back to the parent `Entry`.
        priorities:
            List of frequency tags attached to this reading form. From `<re_pri>`.
    """

    __tablename__ = "reading"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entry.id"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    no_kanji: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    entry: Mapped["Entry"] = relationship(back_populates="readings")
    priorities: Mapped[list["EntryPriority"]] = relationship(back_populates="reading", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("entry_id", "text", name="uix_reading_entry_text"),
        Index("ix_reading_text", "text"),
    )


class EntryPriority(Base):
    """Represents a frequency tag attached to a kanji or reading.

    JMdict uses `<ke_pri>` (kanji) and `<re_pri>` (reading). We store both in one table:
      - If the tag belongs to a kanji form: `kanji_id` is set (and `reading_id` is NULL).
      - If the tag belongs to a reading form: `reading_id` is set (and `kanji_id` is NULL).

    Attributes:
        id:
            Primary key.
        entry_id:
            Foreign key to `Entry`.
        kanji_id:
            Foreign key to `Kanji` when this priority is for a kanji form; NULL otherwise.
        reading_id:
            Foreign key to `Reading` when this priority is for a reading form; NULL otherwise.
        raw:
            The original priority token (e.g., 'nf14', 'news1', 'ichi1').

        kanji:
            Relationship back to the `Kanji` (if `kanji_id` is set).
        reading:
            Relationship back to the `Reading` (if `reading_id` is set).
    """

    __tablename__ = "entry_priority"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entry.id"), nullable=False, index=True)
    kanji_id: Mapped[Optional[int]] = mapped_column(ForeignKey("kanji.id"), index=True)
    reading_id: Mapped[Optional[int]] = mapped_column(ForeignKey("reading.id"), index=True)
    raw: Mapped[str] = mapped_column(String, nullable=False)

    kanji: Mapped[Optional["Kanji"]] = relationship(back_populates="priorities")
    reading: Mapped[Optional["Reading"]] = relationship(back_populates="priorities")

    __table_args__ = (
        # Exactly one target must be set (XOR)
        CheckConstraint(
            "(kanji_id IS NOT NULL) <> (reading_id IS NOT NULL)",
            name="ck_priority_exclusive_target",
        ),
        # Avoid duplicates on either side
        UniqueConstraint("kanji_id", "raw", name="uix_priority_kanji_raw"),
        UniqueConstraint("reading_id", "raw", name="uix_priority_reading_raw"),
        Index("ix_priority_raw", "raw"),
    )


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

    entry: Mapped["Entry"] = relationship(back_populates="senses")
    glosses: Mapped[list["Gloss"]] = relationship(back_populates="sense", cascade="all, delete-orphan")
    pos: Mapped[list["SensePOS"]] = relationship(back_populates="sense", cascade="all, delete-orphan")


class Gloss(Base):
    """Represents a gloss inside a sense `<gloss>`.

    Attributes:
        id:
            Primary key.
        sense_id:
            Foreign key to the Sense it belongs to.
        order:
            1-based position of the gloss within the sense.
        text:
            The gloss text (definition). From the content of `<gloss>`.
        lang:
            Language of the gloss (g_lang). Defaults to 'eng' in JMdict_e.

        sense:
            Relationship back to the parent `Sense`.
    """

    __tablename__ = "gloss"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sense_id: Mapped[int] = mapped_column(ForeignKey("sense.id"), nullable=False, index=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    lang: Mapped[str] = mapped_column(String, nullable=False, default="eng")

    sense: Mapped["Sense"] = relationship(back_populates="glosses")

    __table_args__ = (Index("ix_gloss_text", "text"),)


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

    sense: Mapped["Sense"] = relationship(back_populates="pos")

    __table_args__ = (UniqueConstraint("sense_id", "tag", name="uix_sense_pos_once"),)


class ReadingRestriction(Base):
    """Represents a VALID reading-kanji pairing for an entry `<re_restr>`.

    Attributes:
        id:
            Primary key.
        entry_id:
            Foreign key to `Entry`.
        reading_id:
            Foreign key to the `Reading`.
        kanji_id:
            Foreign key to the `Kanji`.

        entry:
            Relationship back to the parent `Entry`.
    """

    __tablename__ = "reading_restriction"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("entry.id"), nullable=False, index=True)
    reading_id: Mapped[int] = mapped_column(ForeignKey("reading.id"), nullable=False, index=True)
    kanji_id: Mapped[int] = mapped_column(ForeignKey("kanji.id"), nullable=False, index=True)

    entry: Mapped["Entry"] = relationship(back_populates="reading_restrictions")

    __table_args__ = (UniqueConstraint("entry_id", "reading_id", "kanji_id", name="uix_rrestr_unique"),)
