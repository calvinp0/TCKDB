"""TCKDB backend app models transition state module"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from tckdb.backend.app.db.base_class import AuditMixin, Base
from tckdb.backend.app.models.associations import (
    transition_state_authors,
    transition_state_reviewers,
)
from tckdb.backend.app.models.common import MsgpackExt


class TransitionState(Base, AuditMixin):
    """A class for representing a Transition State entry."""

    __tablename__ = "transition_state"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    label = Column(String(255), nullable=True)
    charge = Column(Integer, nullable=False)
    multiplicity = Column(Integer, nullable=False)
    coordinates = Column(MsgpackExt, nullable=False)

    opt_level_id = Column(Integer, ForeignKey("level.id"), nullable=True)
    opt_level = relationship("Level", backref="ts_opt", foreign_keys=[opt_level_id])
    freq_level_id = Column(Integer, ForeignKey("level.id"), nullable=True)
    freq_level = relationship("Level", backref="ts_freq", foreign_keys=[freq_level_id])
    sp_level_id = Column(Integer, ForeignKey("level.id"), nullable=False)
    sp_level = relationship("Level", backref="ts_sp", foreign_keys=[sp_level_id])

    opt_ess_id = Column(Integer, ForeignKey("ess.id"), nullable=True)
    opt_ess = relationship("ESS", backref="ts_opt", foreign_keys=[opt_ess_id])
    freq_ess_id = Column(Integer, ForeignKey("ess.id"), nullable=True)
    freq_ess = relationship("ESS", backref="ts_freq", foreign_keys=[freq_ess_id])
    sp_ess_id = Column(Integer, ForeignKey("ess.id"), nullable=False)
    sp_ess = relationship("ESS", backref="ts_sp", foreign_keys=[sp_ess_id])

    opt_path = Column(String(5000), nullable=True)
    freq_path = Column(String(5000), nullable=True)
    sp_path = Column(String(5000), nullable=False)

    authors = relationship(
        "Person",
        secondary=transition_state_authors,
        backref="authors_transition_states",
    )
    reviewers = relationship(
        "Person",
        secondary=transition_state_reviewers,
        backref="reviewers_transition_states",
    )

    def __str__(self) -> str:  # pragma: no cover - simple string representation
        return f"<TransitionState(id={self.id}, label={self.label})>"
