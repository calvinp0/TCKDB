"""TCKDB backend app models transition state module"""

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from tckdb.backend.app.db.base_class import AuditMixin, Base
from tckdb.backend.app.models.associations import (
    transition_state_authors,
    transition_state_reviewers,
)
from tckdb.backend.app.models.common import (
    MsgpackExt,
)  # use JSONB/MsgpackExt as in the rest


class TransitionState(Base, AuditMixin):
    """Transition state (TS) identity + intrinsic properties.
    Calculation-specific details live in QCFile rows linked via transition_state_id.
    """

    __tablename__ = "transition_state"

    id = Column(Integer, primary_key=True, index=True, nullable=False)

    # Identifiers / basic quantum numbers
    label = Column(String(255), nullable=True)
    charge = Column(Integer, nullable=False)
    multiplicity = Column(Integer, nullable=False)

    # TS 3D conformer
    coordinates = Column(
        MsgpackExt, nullable=False
    )  # ordered atoms XYZ (like Species.coordinates)
    z_matrix = Column(MsgpackExt, nullable=True)  # optional ordered atoms Z-matrix
    external_symmetry = Column(Integer, nullable=True)
    optical_isomers = Column(Integer, nullable=True)
    point_group = Column(String(16), nullable=True)

    # TS status / provenance notes (not method/basis — that stays in QCFile)
    is_lowest_ts = Column(Boolean, nullable=True)  # “as far as author knows”
    determination_note = Column(
        String(1000), nullable=True
    )  # how the TS was determined, unsuccessful methods, etc.
    active_space = Column(
        MsgpackExt, nullable=True
    )  # {'electrons': int, 'orbitals': int} when MR used

    # Energy
    E0 = Column(Float, nullable=True)  # kJ/mol, after ZPE/corrections
    barrierless = Column(Boolean, nullable=True)

    # Modes (TS)
    rotational_constants = Column(MsgpackExt, nullable=True)
    hessian = Column(
        MsgpackExt, nullable=True
    )  # lower triangle; required for polyatomics
    frequencies = Column(MsgpackExt, nullable=True)  # unscaled/unprojected
    scaled_projected_frequencies = Column(MsgpackExt, nullable=True)
    normal_displacement_modes = Column(MsgpackExt, nullable=True)

    # Which rotors weren’t modeled because they break the TS, etc., live inside your torsion dicts’ `invalidated`
    torsions = Column(
        MsgpackExt, nullable=True
    )  # same schema you validated for Species

    # IRC
    irc_trajectories = Column(
        MsgpackExt, nullable=True
    )  # two lists of coordinates dicts

    # Optional: frequency scaling factor used for this TS (many TS share one FreqScale)
    freq_scale_id = Column(Integer, ForeignKey("freqscale.id"), nullable=True)
    freq_scale = relationship("FreqScale")

    # Files (one-to-many; holds opt/freq/sp/irc files + Level/ESS)
    qc_files = relationship("QCFile", back_populates="transition_state")

    # People
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

    def __str__(self) -> str:  # pragma: no cover
        return f"<TransitionState(id={self.id}, label={self.label})>"
