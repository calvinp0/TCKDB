# reaction_entry_well.py
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from tckdb.backend.app.db.base_class import Base
from tckdb.backend.app.models.common import MsgpackExt


class ReactionEntryWell(Base):
    __tablename__ = "reaction_entry_well"

    id = Column(Integer, primary_key=True)
    reaction_entry_id = Column(
        Integer,
        ForeignKey("reaction_entry.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    side = Column(String(16), nullable=False)  # "reactant" or "product"
    pos = Column(Integer, nullable=False, default=1)  # ordering within the side

    # exactly one of these:
    species_entry_id = Column(
        Integer,
        ForeignKey("species_entry.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    vdw_entry_id = Column(
        Integer,
        ForeignKey("vdw_entry.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    __table_args__ = (
        CheckConstraint(
            "(species_entry_id IS NOT NULL)::int + (vdw_entry_id IS NOT NULL)::int = 1",
            name="reaction_entry_well_oneof_chk",
        ),
        Index("rxn_entry_well_side_pos_idx", "reaction_entry_id", "side", "pos"),
    )
