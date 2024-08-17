"""Initial migration

Revision ID: 22d655286e5f
Revises:
Create Date: 2024-08-17 22:10:43.374307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '22d655286e5f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account_ivashko',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('balance', sa.BIGINT(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['user_id'], ['users_ivashko.id'], ),
    schema='transaction_ivashko'
    )
    op.create_table('transactions_ivashko',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.BIGINT(), nullable=False),
    sa.Column('type', sa.Enum('DEBIT', 'CREDIT', name='transactiontype'), nullable=False),
    sa.Column('balance_after', sa.BIGINT(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['transaction_ivashko.account_ivashko.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='transaction_ivashko'
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('account_ivashko', schema='transactions_ivashko')
    op.drop_table('transactions_ivashko', schema='transactions_ivashko')
    # ### end Alembic commands ###
