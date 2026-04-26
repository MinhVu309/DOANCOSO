"""add user_conditions table

Revision ID: a3f8b2e1d9c4
Revises: cfa1616534cf
Create Date: 2026-04-26 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = 'a3f8b2e1d9c4'
down_revision: Union[str, None] = 'cfa1616534cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_conditions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('condition_name', sa.String(200), nullable=False),
        sa.Column('occurrence_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('avg_confidence', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('first_seen_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_seen_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('confirmed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'condition_name', name='uq_user_condition'),
    )
    op.create_index('ix_user_conditions_user_id', 'user_conditions', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_user_conditions_user_id', table_name='user_conditions')
    op.drop_table('user_conditions')
