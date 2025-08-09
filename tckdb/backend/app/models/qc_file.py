"""Model for storing quantum chemistry calculation files."""

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Enum,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from tckdb.backend.app.db.base_class import AuditMixin, Base

CalcType = Enum("opt", "freq", "scan", "irc", "sp", name="calc_type_enum")
StatusType = Enum("pending", "ok", "failed", name="status_enum")


class QCFile(Base, AuditMixin):
    """Store input and output files for quantum chemistry calculations."""

    __tablename__ = "qc_file"

    id = Column(Integer, primary_key=True, index=True, nullable=False)

    species_id = Column(
        Integer, ForeignKey("species.id", ondelete="SET NULL"), index=True
    )
    transition_state_id = Column(
        Integer, ForeignKey("transition_state.id", ondelete="SET NULL"), index=True
    )
    np_species_id = Column(
        Integer, ForeignKey("nonphysicalspecies.id", ondelete="SET NULL"), index=True
    )

    calc_type = Column(CalcType, nullable=False)
    status = Column(StatusType, nullable=False)
    level_id = Column(Integer, ForeignKey("level.id"), nullable=False, index=True)
    ess_id = Column(Integer, ForeignKey("ess.id"), nullable=False, index=True)

    input_name = Column(String(255))
    output_name = Column(String(255))
    input_file = Column(LargeBinary)
    output_file = Column(LargeBinary)
    compressed = Column(Boolean, default=True, nullable=False)
    checksum = Column(String(64), nullable=False)

    __table_args__ = (
        UniqueConstraint("checksum", name="uq_qcfile_checksum"),
        CheckConstraint(
            "(species_id IS NOT NULL)::int + "
            "(transition_state_id IS NOT NULL)::int + "
            "(np_species_id IS NOT NULL)::int = 1",
            name="qc_owner_oneof_chk",
        ),
    )

    species = relationship("Species", back_populates="qc_files")
    transition_state = relationship("TransitionState", back_populates="qc_files")
    np_species = relationship("NonPhysicalSpecies", back_populates="qc_files")
    level = relationship("Level")
    ess = relationship("ESS")
