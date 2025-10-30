"""search indexes

Revision ID: b2ceaffcb2fe
Revises: 7f2f4b07283d
Create Date: 2025-10-30 22:32:19.096599

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2ceaffcb2fe"
down_revision: str | Sequence[str] | None = "7f2f4b07283d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    op.create_index(
        "ix_readings_text_trgm",
        "readings",
        ["text"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"text": "gin_trgm_ops"},
    )
    op.create_index(
        "ix_kanjis_text_trgm",
        "kanjis",
        ["text"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"text": "gin_trgm_ops"},
    )

    op.execute("CREATE INDEX ix_glosses_text_fts ON glosses USING GIN (to_tsvector('english', coalesce(text, '')))")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS ix_glosses_text_fts")

    op.drop_index("ix_kanjis_text_trgm", table_name="kanjis")
    op.drop_index("ix_readings_text_trgm", table_name="readings")
