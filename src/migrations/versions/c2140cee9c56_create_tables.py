"""create tables

Revision ID: c2140cee9c56
Revises:
Create Date: 2025-10-30 09:23:52.778478
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c2140cee9c56"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    # --- entries ---
    op.create_table(
        "entries",
        sa.Column("sequence", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("is_common", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )

    # --- entry_elements ---
    op.create_table(
        "entry_elements",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column(
            "entry_sequence",
            sa.Integer(),
            sa.ForeignKey("entries.sequence", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("is_kanji", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("no_true_reading", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.create_index("ix_entry_elements_entry_sequence", "entry_elements", ["entry_sequence"])

    # --- element_priorities ---
    op.create_table(
        "element_priorities",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column(
            "element_id",
            sa.Integer(),
            sa.ForeignKey("entry_elements.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("priority_type", sa.String(length=16), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.UniqueConstraint("element_id", "priority_type", "level", name="uq_element_priority"),
    )
    op.create_index("ix_element_priorities_element_id", "element_priorities", ["element_id"])

    # --- element_reading_info ---
    op.create_table(
        "element_reading_info",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column(
            "element_id",
            sa.Integer(),
            sa.ForeignKey("entry_elements.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("info", sa.String(length=16), nullable=False),
        sa.UniqueConstraint("element_id", "info", name="uq_element_reading_info"),
    )
    op.create_index("ix_element_reading_info_element_id", "element_reading_info", ["element_id"])

    # --- senses ---
    op.create_table(
        "senses",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column(
            "entry_sequence",
            sa.Integer(),
            sa.ForeignKey("entries.sequence", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("sense_index", sa.Integer(), nullable=True),
        sa.Column("misc", sa.String(length=16), nullable=True),
        sa.Column("field", sa.String(length=16), nullable=True),
        sa.Column("dialect", sa.String(length=16), nullable=True),
        sa.Column("gairaigo", sa.String(length=8), nullable=True),
        sa.Column("antonym", sa.String(), nullable=True),
        sa.Column("xref", sa.String(), nullable=True),
        sa.Column("information", sa.String(), nullable=True),
    )
    op.create_index("ix_senses_entry_sequence", "senses", ["entry_sequence"])

    # --- sense_parts_of_speech ---
    op.create_table(
        "sense_parts_of_speech",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("sense_id", sa.Integer(), sa.ForeignKey("senses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("pos", sa.String(length=24), nullable=False),
        sa.UniqueConstraint("sense_id", "pos", name="uq_sense_pos"),
    )
    op.create_index("ix_sense_parts_of_speech_sense_id", "sense_parts_of_speech", ["sense_id"])

    # --- glosses ---
    op.create_table(
        "glosses",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("sense_id", sa.Integer(), sa.ForeignKey("senses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("gtype", sa.String(length=8), nullable=True),
        sa.Column("text", sa.String(), nullable=False),
    )
    op.create_index("ix_glosses_sense_id", "glosses", ["sense_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_glosses_sense_id", table_name="glosses")
    op.drop_table("glosses")

    op.drop_index("ix_sense_parts_of_speech_sense_id", table_name="sense_parts_of_speech")
    op.drop_table("sense_parts_of_speech")

    op.drop_index("ix_senses_entry_sequence", table_name="senses")
    op.drop_table("senses")

    op.drop_index("ix_element_reading_info_element_id", table_name="element_reading_info")
    op.drop_table("element_reading_info")

    op.drop_index("ix_element_priorities_element_id", table_name="element_priorities")
    op.drop_table("element_priorities")

    op.drop_index("ix_entry_elements_entry_sequence", table_name="entry_elements")
    op.drop_table("entry_elements")

    op.drop_table("entries")
