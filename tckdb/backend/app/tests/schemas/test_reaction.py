"""Tests for the Reaction schema"""

from tckdb.backend.app.schemas.reaction import ReactionBase, ReactionParticipantBase


def test_reaction_schema():
    """Test creating a ReactionBase instance"""
    rxn = ReactionBase(
        formal_charge=0,
        multiplicity=1,
        participants=[
            ReactionParticipantBase(step_index=0, role="reactant", species_id=1),
            ReactionParticipantBase(step_index=1, role="product", species_id=2),
        ],
    )
    assert rxn.participants[0].species_id == 1
    assert rxn.participants[1].species_id == 2

    ReactionBase(formal_charge=0, multiplicity=1)
