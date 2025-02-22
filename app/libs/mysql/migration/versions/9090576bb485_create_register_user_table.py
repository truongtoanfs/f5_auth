"""create register, user table

Revision ID: 9090576bb485
Revises: 
Create Date: 2024-12-20 15:34:28.097304

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9090576bb485"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "register",
        sa.Column("id", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("password_expired_at", sa.DateTime(), nullable=False),
        sa.Column("is_confirmed", sa.Boolean(), nullable=False),
        sa.Column("confirmed_at", sa.DateTime(), nullable=True),
        sa.Column("resend_verification_count", sa.Integer(), nullable=False),
        sa.Column("resend_verification_blocked_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_register_email"), "register", ["email"], unique=False)
    op.create_table(
        "user",
        sa.Column("id", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("password_expired", sa.Boolean(), nullable=False),
        sa.Column("password_expired_at", sa.DateTime(), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("fullname", sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_register_email"), table_name="register")
    op.drop_table("register")
    # ### end Alembic commands ###
