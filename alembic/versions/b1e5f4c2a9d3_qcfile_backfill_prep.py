"""qcfile backfill prep

Revision ID: b1e5f4c2a9d3
Revises: aa7159c17074
Create Date: 2025-08-09

Purpose:
 - Add ENUM types for qc_file.calc_type / status
 - Alter qc_file columns to ENUM
 - Add unique + check constraints
 - Add named indexes
 - Backfill qc_file from existing species calc-specific ESS/Level columns (phase 1 keeps old columns)

Downgrade reverses structural changes (does NOT delete backfilled rows).
"""

from __future__ import annotations

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "b1e5f4c2a9d3"
down_revision: Union[str, None] = "aa7159c17074"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

calc_type_enum = sa.Enum("opt", "freq", "scan", "irc", "sp", name="calc_type_enum")
status_enum = sa.Enum("pending", "ok", "failed", name="status_enum")

CALC_TYPES = ["opt", "freq", "scan", "irc", "sp"]


def upgrade() -> None:
    bind = op.get_bind()

    # Create enums if not exist
    calc_type_enum.create(bind, checkfirst=True)
    status_enum.create(bind, checkfirst=True)

    # Alter columns to use ENUM (only if existing type is not already ENUM)
    with op.batch_alter_table("qc_file") as batch_op:
        batch_op.alter_column(
            "calc_type",
            existing_type=sa.String(length=20),
            type_=calc_type_enum,
            existing_nullable=False,
        )
        batch_op.alter_column(
            "status",
            existing_type=sa.String(length=20),
            type_=status_enum,
            existing_nullable=False,
        )

    # Constraints / indexes (id index may already exist, keep others)
    op.create_unique_constraint(
        "uq_qcfile_checksum",
        "qc_file",
        ["checksum"],
    )
    op.create_check_constraint(
        "qc_owner_oneof_chk",
        "qc_file",
        "(CASE WHEN species_id IS NOT NULL THEN 1 ELSE 0 END + "
        "CASE WHEN transition_state_id IS NOT NULL THEN 1 ELSE 0 END + "
        "CASE WHEN np_species_id IS NOT NULL THEN 1 ELSE 0 END) = 1",
    )
    for idx_name, col in [
        ("qc_file_species_id_idx", "species_id"),
        ("qc_file_calc_type_idx", "calc_type"),
        ("qc_file_status_idx", "status"),
        ("qc_file_level_id_idx", "level_id"),
        ("qc_file_ess_id_idx", "ess_id"),
    ]:
        op.create_index(idx_name, "qc_file", [col], unique=False)

    # Data backfill from species table
    # Use md5(species.id || ':' || calc_type) as deterministic checksum placeholder
    for calc in CALC_TYPES:
        # calc is from a fixed trusted list above; build column names explicitly
        ess_col = f"{calc}_ess_id"
        level_col = f"{calc}_level_id"
        # Controlled construction (whitelisted identifiers) - nosec B608
        insert_sql = (
            "INSERT INTO qc_file (species_id, calc_type, ess_id, level_id, status, compressed, checksum, created_at, updated_at) "  # nosec B608
            "SELECT s.id, '{calc}', s.{ess_col}, s.{level_col}, 'ok', TRUE, "
            "md5(s.id::text || ':{calc}'), now(), now() "
            "FROM species s "
            "WHERE s.{ess_col} IS NOT NULL AND s.{level_col} IS NOT NULL "
            "AND NOT EXISTS (SELECT 1 FROM qc_file q WHERE q.species_id = s.id AND q.calc_type = '{calc}')"
        ).format(calc=calc, ess_col=ess_col, level_col=level_col)
        op.execute(text(insert_sql))


def downgrade() -> None:
    # Structural downgrade; keep backfilled data
    for idx in [
        "qc_file_species_id_idx",
        "qc_file_calc_type_idx",
        "qc_file_status_idx",
        "qc_file_level_id_idx",
        "qc_file_ess_id_idx",
    ]:
        op.drop_index(idx, table_name="qc_file")

    op.drop_constraint("qc_owner_oneof_chk", "qc_file", type_="check")
    op.drop_constraint("uq_qcfile_checksum", "qc_file", type_="unique")

    # Revert columns to String
    with op.batch_alter_table("qc_file") as batch_op:
        batch_op.alter_column(
            "status",
            existing_type=status_enum,
            type_=sa.String(length=20),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "calc_type",
            existing_type=calc_type_enum,
            type_=sa.String(length=20),
            existing_nullable=False,
        )

    # Drop enums (optional) - keep for safety; comment out if you prefer to retain
    # status_enum.drop(op.get_bind(), checkfirst=True)
    # calc_type_enum.drop(op.get_bind(), checkfirst=True)
