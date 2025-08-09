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

    qc_files = relationship("QCFile", back_populates="transition_state")

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
