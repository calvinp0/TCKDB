from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from tckdb.backend.app.db.base_class import Base


class Torsion(Base):
    __tablename__ = "torsion"

    id = Column(Integer, primary_key=True, index=True)

    computation_type = Column(String, nullable=False)
    dimension = Column(Integer, nullable=False)
    constraints = Column(JSONB, nullable=True)  # dict
    symmetry = Column(Integer, nullable=True)
    treatment = Column(String, nullable=False)
    torsions = Column(JSONB, nullable=False)  # list[list[int]]
    top = Column(JSONB, nullable=False)  # list[int]
    energies = Column(JSONB, nullable=False)  # ND list of floats
    resolution = Column(JSONB, nullable=False)  # float or list[float]
    trajectory = Column(JSONB, nullable=False)  # ND list of coordinates dicts
    invalidated = Column(String, nullable=True)

    # Parent link: exactly one of these must be set
    species_entry_id = Column(
        Integer, ForeignKey("species_entry.id"), nullable=True, index=True
    )
    transition_state_id = Column(
        Integer, ForeignKey("transition_state.id"), nullable=True, index=True
    )

    species_entry = relationship("SpeciesEntry", back_populates="torsions")
    transition_state = relationship("TransitionState", back_populates="torsions")

    __table_args__ = (
        CheckConstraint(
            "(species_entry_id IS NOT NULL)::int + (transition_state_id IS NOT NULL)::int = 1",
            name="torsion_one_parent_chk",
        ),
    )
