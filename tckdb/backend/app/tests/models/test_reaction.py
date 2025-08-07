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
        ReactionParticipant(step_index=1, role="ts", ts_id=4),
        ReactionParticipant(step_index=2, role="product", species_id=3),
    ]
    entry = ReactionEntry(
        reaction=rxn,
        kinetics={"A": 1.0},
        kinetics_fit={"A": 1.0},
        fit_error={"A": 0.1},
        atom_mapping={"1": "1"},
        uncertainties={"A": 0.2},
    )
    assert len(rxn.participants) == 4
    assert rxn.participants[0].species_id == 1
    assert rxn.participants[1].vdw_id == 2
    assert rxn.participants[2].ts_id == 4
    assert rxn.participants[3].species_id == 3
    assert rxn.entries[0] is entry
    assert str(rxn) == "<Reaction(id=None, charge=0)>"
