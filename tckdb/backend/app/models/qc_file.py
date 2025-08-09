"""Model for storing quantum chemistry calculation files."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from tckdb.backend.app.db.base_class import AuditMixin, Base


class QCFile(Base, AuditMixin):
    """A model to store input and output files for quantum chemistry calculations."""

    __tablename__ = "qc_file"

    id = Column(Integer, primary_key=True, index=True, nullable=False)

    species_id = Column(Integer, ForeignKey("species.id"), nullable=True)
    transition_state_id = Column(
        Integer, ForeignKey("transition_state.id"), nullable=True
    )
    np_species_id = Column(Integer, ForeignKey("nonphysicalspecies.id"), nullable=True)

    calc_type = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    level_id = Column(Integer, ForeignKey("level.id"), nullable=False)
    ess_id = Column(Integer, ForeignKey("ess.id"), nullable=False)

    input_name = Column(String(255), nullable=True)
    output_name = Column(String(255), nullable=True)
    input_file = Column(LargeBinary, nullable=True)
    output_file = Column(LargeBinary, nullable=True)
    compressed = Column(Boolean, default=True, nullable=False)
    checksum = Column(String(64), nullable=False)

    species = relationship("Species", back_populates="qc_files")
    transition_state = relationship("TransitionState", back_populates="qc_files")
    np_species = relationship("NonPhysicalSpecies", back_populates="qc_files")
    level = relationship("Level")
    ess = relationship("ESS")
