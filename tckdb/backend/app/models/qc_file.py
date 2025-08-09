import sqlalchemy as sa
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    LargeBinary,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from tckdb.backend.app.db.base_class import AuditMixin, Base

# PostgreSQL enums via SQLAlchemy
CalcType = sa.Enum("opt", "freq", "scan", "irc", "sp", name="calc_type_enum")
StatusType = sa.Enum("pending", "ok", "failed", name="status_enum")


class QCFile(Base, AuditMixin):
    __tablename__ = "qc_file"

    id = Column(Integer, primary_key=True, index=True, nullable=False)

    # exactly one owner is set
    species_id = Column(
        Integer, ForeignKey("species.id", ondelete="CASCADE"), index=True
    )
    transition_state_id = Column(
        Integer, ForeignKey("transition_state.id", ondelete="CASCADE"), index=True
    )
    np_species_id = Column(
        Integer, ForeignKey("nonphysicalspecies.id", ondelete="CASCADE"), index=True
    )
    vdw_entry_id = Column(
        Integer, ForeignKey("vdw_entry.id", ondelete="CASCADE"), index=True
    )

    calc_type = Column(CalcType, nullable=False, index=True)
    status = Column(StatusType, nullable=False, index=True)

    level_id = Column(Integer, ForeignKey("level.id"), nullable=False, index=True)
    ess_id = Column(Integer, ForeignKey("ess.id"), nullable=False, index=True)

    input_name = Column(String(255))
    output_name = Column(String(255))
    input_file = Column(LargeBinary)
    output_file = Column(LargeBinary)
    compressed = Column(Boolean, nullable=False, server_default=sa.text("true"))
    checksum = Column(String(64), nullable=False)

    species = relationship("Species", back_populates="qc_files")
    transition_state = relationship("TransitionState", back_populates="qc_files")
    np_species = relationship("NonPhysicalSpecies", back_populates="qc_files")
    vdw_entry = relationship("VDWEntry", back_populates="qc_files")
    level = relationship("Level")
    ess = relationship("ESS")

    __table_args__ = (
        UniqueConstraint("checksum", name="uq_qcfile_checksum"),
        # exactly one of the four owners must be set
        CheckConstraint(
            "(species_id IS NOT NULL)::int + "
            "(transition_state_id IS NOT NULL)::int + "
            "(np_species_id IS NOT NULL)::int + "
            "(vdw_entry_id IS NOT NULL)::int = 1",
            name="qc_owner_oneof_chk",
        ),
        # at most one file per owner+calc_type
        Index(
            "uq_qc_species_type",
            "species_id",
            "calc_type",
            unique=True,
            postgresql_where=sa.text("species_id IS NOT NULL"),
        ),
        Index(
            "uq_qc_ts_type",
            "transition_state_id",
            "calc_type",
            unique=True,
            postgresql_where=sa.text("transition_state_id IS NOT NULL"),
        ),
        Index(
            "uq_qc_np_species_type",
            "np_species_id",
            "calc_type",
            unique=True,
            postgresql_where=sa.text("np_species_id IS NOT NULL"),
        ),
        Index(
            "uq_qc_vdw_type",
            "vdw_entry_id",
            "calc_type",
            unique=True,
            postgresql_where=sa.text("vdw_entry_id IS NOT NULL"),
        ),
    )
