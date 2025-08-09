from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from tckdb.backend.app.db.base_class import Base
from tckdb.backend.app.models.common import MsgpackExt
from sqlalchemy.sql import func


class VDW(Base):
    __tablename__ = "vdw"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    tckdb_vdw_uid = Column(
        String(64), nullable=False, unique=True
    )  # Unique VDW identifier

    # Chemical identifiers block
    inchi_augmented_list = Column(
        ARRAY(String), nullable=False
    )  # list of augmented InChI for the components
    molecular_formula = Column(String(255), nullable=True)
    molecular_weight = Column(Float, nullable=True)
    charge = Column(Integer, nullable=False)
    multiplicity = Column(Integer, nullable=False)

    # User labels (could be several names)
    labels = Column(ARRAY(String), nullable=True)

    # Optional orientation for multi-fragment wells
    fragment_orientation = Column(MsgpackExt, nullable=True)

    # Relations
    entries = relationship(
        "VDWEntry", back_populates="vdw", cascade="all, delete-orphan"
    )

    # Optional: link wells to reactions (many-to-many)
    reactions = relationship(
        "Reaction", secondary="reaction_vdw", back_populates="vdw_wells"
    )


class VDWEntry(Base):
    __tablename__ = "vdw_entry"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    tckdb_vdw_entry_uid = Column(String(64), nullable=False, unique=True)

    vdw_id = Column(Integer, ForeignKey("vdw.id", ondelete="CASCADE"), nullable=False)
    vdw = relationship("VDW", back_populates="entries")

    # General / provenance
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    software_note = Column(String(255), nullable=True)  # “ARC x.y”, “Script v1.2”, etc.
    citation = Column(String(500), nullable=True)

    # Geometry block
    xyz = Column(MsgpackExt, nullable=True)  # ordered atoms geometry
    z_matrix = Column(MsgpackExt, nullable=True)  # ordered atoms z-matrix
    external_symmetry = Column(Integer, nullable=True)
    optical_isomers = Column(Integer, nullable=True)
    point_group = Column(String(16), nullable=True)

    # Energy block
    E0 = Column(Float, nullable=True)

    # Modes (same structure as SpeciesEntry)
    modes = Column(MsgpackExt, nullable=True)

    # Authors / Reviewers (reuse Person tables like Species/TS)
    authors = relationship(
        "Person", secondary="vdwentry_authors", backref="authors_vdwentries"
    )
    reviewers = relationship(
        "Person", secondary="vdwentry_reviewers", backref="reviewers_vdwentries"
    )

    # Files: handled via QCFile (see below)
    qc_files = relationship("QCFile", back_populates="vdw_entry")
