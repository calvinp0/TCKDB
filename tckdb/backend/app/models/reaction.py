"""TCKDB backend app models reaction module"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from tckdb.backend.app.db.base_class import AuditMixin, Base
from tckdb.backend.app.models.associations import (
    reaction_authors,
    reaction_reviewers,
    reaction_entry_authors,
    reaction_entry_reviewers,
)
from tckdb.backend.app.models.common import MsgpackExt


class Reaction(Base, AuditMixin):
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
    authors = relationship(
        "Person", secondary=reaction_authors, backref="authors_reactions"
    )
    reviewers = relationship(
        "Person", secondary=reaction_reviewers, backref="reviewers_reactions"
    )

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"<{self.__class__.__name__}(id={self.id}, charge={self.formal_charge})>"


class ReactionParticipant(Base):
    """Association table linking reactions to species, VDW wells, or transition states"""

    __tablename__ = "reaction_participant"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    reaction_id = Column(Integer, ForeignKey("reaction.id"), nullable=False)
    step_index = Column(Integer, nullable=False)
    role = Column(String(50), nullable=False)
    species_id = Column(Integer, ForeignKey("species.id"), nullable=True)
    ts_id = Column(Integer, ForeignKey("transition_state.id"), nullable=True)
    vdw_id = Column(Integer, ForeignKey("vdw.id"), nullable=True)

    reaction = relationship("Reaction", back_populates="participants")
    species = relationship("Species")
    transition_state = relationship("TransitionState")
    vdw = relationship("VDW")


class ReactionEntry(Base, AuditMixin):
    """A class representing a computed entry for a reaction"""

    __tablename__ = "reaction_entry"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    reaction_id = Column(Integer, ForeignKey("reaction.id"), nullable=False)
    kinetics = Column(MsgpackExt, nullable=True)
    kinetics_fit = Column(MsgpackExt, nullable=True)
    fit_error = Column(MsgpackExt, nullable=True)
    atom_mapping = Column(MsgpackExt, nullable=True)
    uncertainties = Column(MsgpackExt, nullable=True)
    ess_id = Column(Integer, ForeignKey("ess.id"), nullable=True)
    literature_id = Column(Integer, ForeignKey("literature.id"), nullable=True)

    reaction = relationship("Reaction", back_populates="entries")
    ess = relationship("ESS")
    literature = relationship("Literature")
    authors = relationship(
        "Person", secondary=reaction_entry_authors, backref="authors_reaction_entries"
    )
    reviewers = relationship(
        "Person",
        secondary=reaction_entry_reviewers,
        backref="reviewers_reaction_entries",
    )

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return (
            f"<{self.__class__.__name__}(id={self.id}, reaction_id={self.reaction_id})>"
        )
