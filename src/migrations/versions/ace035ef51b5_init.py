"""init

Revision ID: ace035ef51b5
Revises:
Create Date: 2025-10-30 16:13:49.894923

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSON

revision: str = "ace035ef51b5"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "words",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "kanjis",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("is_common", sa.Boolean(), nullable=False),
        sa.Column("tags", JSON, nullable=False),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_kanjis_word_id"), "kanjis", ["word_id"], unique=False)
    op.create_index(op.f("ix_kanjis_text"), "kanjis", ["text"], unique=False)

    op.create_table(
        "readings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("is_common", sa.Boolean(), nullable=False),
        sa.Column("tags", JSON, nullable=False),
        sa.Column("applies_to_kanji", JSON, nullable=False),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_readings_word_id"), "readings", ["word_id"], unique=False)
    op.create_index(op.f("ix_readings_text"), "readings", ["text"], unique=False)

    op.create_table(
        "senses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("part_of_speech", JSON, nullable=False),
        sa.Column("applies_to_kanji", JSON, nullable=False),
        sa.Column("applies_to_reading", JSON, nullable=False),
        sa.Column("fields", JSON, nullable=False),
        sa.Column("dialects", JSON, nullable=False),
        sa.Column("misc", JSON, nullable=False),
        sa.Column("infos", JSON, nullable=False),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_senses_word_id"), "senses", ["word_id"], unique=False)

    op.create_table(
        "sense_examples",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sense_id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("jpn", sa.String(), nullable=False),
        sa.Column("eng", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["sense_id"], ["senses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sense_examples_sense_id"), "sense_examples", ["sense_id"], unique=False)

    op.create_table(
        "glosses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sense_id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("text", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["sense_id"], ["senses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_glosses_sense_id"), "glosses", ["sense_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_glosses_sense_id"), table_name="glosses")
    op.drop_table("glosses")
    op.drop_index(op.f("ix_sense_examples_sense_id"), table_name="sense_examples")
    op.drop_table("sense_examples")
    op.drop_index(op.f("ix_senses_word_id"), table_name="senses")
    op.drop_table("senses")
    op.drop_index(op.f("ix_readings_text"), table_name="readings")
    op.drop_index(op.f("ix_readings_word_id"), table_name="readings")
    op.drop_table("readings")
    op.drop_index(op.f("ix_kanjis_text"), table_name="kanjis")
    op.drop_index(op.f("ix_kanjis_word_id"), table_name="kanjis")
    op.drop_table("kanjis")
    op.drop_table("words")
