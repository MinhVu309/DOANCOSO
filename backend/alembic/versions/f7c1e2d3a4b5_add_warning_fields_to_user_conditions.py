"""add warning fields to user_conditions

Revision ID: f7c1e2d3a4b5
Revises: a3f8b2e1d9c4
Create Date: 2026-05-08 00:00:00.000000

Adds DSM-5/ICD-11 early-warning fields to user_conditions:
  warning_level, intensity_score, consecutive_days, within_window_days,
  last_warned_at, dsm5_code, icd11_code.

Per [1] APA DSM-5-TR (2022) and [2] WHO ICD-11 CDDR (2024).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'f7c1e2d3a4b5'
down_revision: Union[str, None] = 'a3f8b2e1d9c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_conditions',
        sa.Column('warning_level', sa.String(10), nullable=True))
    op.add_column('user_conditions',
        sa.Column('intensity_score', sa.Float(), nullable=True))
    op.add_column('user_conditions',
        sa.Column('consecutive_days', sa.Integer(), nullable=True))
    op.add_column('user_conditions',
        sa.Column('within_window_days', sa.Integer(), nullable=True))
    op.add_column('user_conditions',
        sa.Column('last_warned_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('user_conditions',
        sa.Column('dsm5_code', sa.String(20), nullable=True))
    op.add_column('user_conditions',
        sa.Column('icd11_code', sa.String(10), nullable=True))


def downgrade() -> None:
    op.drop_column('user_conditions', 'icd11_code')
    op.drop_column('user_conditions', 'dsm5_code')
    op.drop_column('user_conditions', 'last_warned_at')
    op.drop_column('user_conditions', 'within_window_days')
    op.drop_column('user_conditions', 'consecutive_days')
    op.drop_column('user_conditions', 'intensity_score')
    op.drop_column('user_conditions', 'warning_level')
