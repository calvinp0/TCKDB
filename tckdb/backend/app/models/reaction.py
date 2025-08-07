"""TCKDB backend app models reaction module"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from tckdb.backend.app.db.base_class import Base
from tckdb.backend.app.models.common import MsgpackExt


class Reaction(Base):
    """A class representing the chemical identity of a reaction"""

    __tablename__ = "reaction"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    formal_charge = Column(Integer, nullable=False)
    multiplicity = Column(Integer, nullable=False)
    family = Column(String(255), nullable=True)
    labels = Column(MsgpackExt, nullable=True)
    reviewer_flags = Column(MsgpackExt, nullable=True)

    participants = relationship(
        "ReactionParticipant", back_populates="reaction", cascade="all, delete-orphan"
    )
    entries = relationship(
        "ReactionEntry", back_populates="reaction", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"<{self.__class__.__name__}(id={self.id}, charge={self.formal_charge})>"


class ReactionParticipant(Base):
    """Association table linking reactions to species, VDW wells, or non-physical species"""

    __tablename__ = "reaction_participant"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    reaction_id = Column(Integer, ForeignKey("reaction.id"), nullable=False)
    step_index = Column(Integer, nullable=False)
    role = Column(String(50), nullable=False)
    species_id = Column(Integer, ForeignKey("species.id"), nullable=True)
    np_species_id = Column(Integer, ForeignKey("nonphysicalspecies.id"), nullable=True)
    vdw_id = Column(Integer, ForeignKey("vdw.id"), nullable=True)

    reaction = relationship("Reaction", back_populates="participants")
    species = relationship("Species")
    np_species = relationship("NonPhysicalSpecies")
    vdw = relationship("VDW")


class ReactionEntry(Base):
    """A class representing a computed entry for a reaction"""

    __tablename__ = "reaction_entry"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    reaction_id = Column(Integer, ForeignKey("reaction.id"), nullable=False)
    kinetics = Column(MsgpackExt, nullable=True)

    reaction = relationship("Reaction", back_populates="entries")

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return (
            f"<{self.__class__.__name__}(id={self.id}, reaction_id={self.reaction_id})>"
        )
