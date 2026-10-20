"""add hero status and created_at

Revision ID: 7c1f2b3a4d5e
Revises: 561a9fefd664
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7c1f2b3a4d5e"
down_revision: Union[str, Sequence[str], None] = "561a9fefd664"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "hero",
        sa.Column("status", sa.String(length=7), nullable=False, server_default="active"),
    )
    op.add_column(
        "hero",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.execute(sa.text("UPDATE hero SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"))
    with op.batch_alter_table("hero") as batch_op:
        batch_op.alter_column("created_at", nullable=False)


def downgrade() -> None:
    op.drop_column("hero", "created_at")
    op.drop_column("hero", "status")
