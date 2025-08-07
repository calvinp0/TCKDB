"""Tests for the Reaction model"""

from tckdb.backend.app.models.reaction import (
    Reaction,
    ReactionEntry,
    ReactionParticipant,
)


def test_reaction_model():
    """Test creating a reaction with multiple participants"""
    rxn = Reaction(formal_charge=0, multiplicity=1, labels=["test"])
    rxn.participants = [
        ReactionParticipant(step_index=0, role="reactant", species_id=1),
        ReactionParticipant(step_index=0, role="reactant", vdw_id=2),
        ReactionParticipant(step_index=1, role="product", species_id=3),
    ]
    entry = ReactionEntry(reaction=rxn, kinetics={"A": 1.0})
    assert len(rxn.participants) == 3
    assert rxn.participants[0].species_id == 1
    assert rxn.participants[2].species_id == 3
    assert rxn.entries[0] is entry
    assert str(rxn) == "<Reaction(id=None, charge=0)>"
