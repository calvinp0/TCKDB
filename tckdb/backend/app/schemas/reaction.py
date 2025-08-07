"""Pydantic schemas for reactions and reaction entries"""

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReactionParticipantBase(BaseModel):
    """Participant in a reaction pathway"""

    step_index: int = Field(..., title="Position along the reaction coordinate")
    role: str = Field(..., title="Participant role (reactant, product, ts, vdw, intermediate)")
    species_id: Optional[int] = Field(None, title="Species identifier")
    ts_id: Optional[int] = Field(None, title="Transition state identifier")
    vdw_id: Optional[int] = Field(None, title="VDW identifier")
    model_config = ConfigDict(extra="forbid")


class ReactionBase(BaseModel):
    """Shared properties for reactions"""

    formal_charge: int = Field(..., title="Overall formal charge")
    multiplicity: int = Field(..., title="Spin multiplicity")
    family: Optional[str] = Field(None, title="RMG reaction family tag")
    labels: Optional[List[str]] = Field(None, title="User labels")
    participants: Optional[List[ReactionParticipantBase]] = Field(
        None, title="Reaction participants"
    )
    reviewer_flags: Optional[Dict[str, str]] = Field(None, title="Reviewer flags")
    model_config = ConfigDict(extra="forbid")

    @field_validator("labels", "participants", mode="before")
    @classmethod
    def ensure_list(cls, value):
        """Ensure list fields are lists"""
        if value is None:
            return []
        return list(value)

    @field_validator("reviewer_flags", mode="before")
    @classmethod
    def ensure_dict(cls, value):
        """Ensure dict fields are dictionaries"""
        return value or dict()


class ReactionCreate(ReactionBase):
    """Create a Reaction item"""

    pass


class ReactionUpdate(ReactionBase):
    """Update a Reaction item"""

    pass


class ReactionInDBBase(ReactionBase):
    """Properties shared by models stored in DB"""

    id: int
    model_config = ConfigDict(from_attributes=True)


class Reaction(ReactionInDBBase):
    """Properties to return to client"""

    pass


class ReactionInDB(ReactionInDBBase):
    """Properties stored in DB"""

    pass


class ReactionEntryBase(BaseModel):
    """Shared properties for reaction entry items"""

    reaction_id: int = Field(..., title="Parent reaction identifier")
    kinetics: Optional[Dict[str, object]] = Field(None, title="Kinetic data")
    kinetics_fit: Optional[Dict[str, object]] = Field(
        None, title="Fitted high-P limit kinetics"
    )
    fit_error: Optional[Dict[str, object]] = Field(
        None, title="Errors introduced by the fit"
    )
    atom_mapping: Optional[Dict[str, object]] = Field(
        None, title="Reaction atom mapping"
    )
    uncertainties: Optional[Dict[str, object]] = Field(
        None, title="Uncertainties and their determination"
    )
    ess_id: Optional[int] = Field(None, title="ESS identifier")
    literature_id: Optional[int] = Field(None, title="Citation identifier")
    model_config = ConfigDict(extra="forbid")


class ReactionEntryCreate(ReactionEntryBase):
    """Create a reaction entry"""

    pass


class ReactionEntryUpdate(ReactionEntryBase):
    """Update a reaction entry"""

    pass


class ReactionEntryInDBBase(ReactionEntryBase):
    """Properties shared by reaction entry models stored in DB"""

    id: int
    model_config = ConfigDict(from_attributes=True)


class ReactionEntry(ReactionEntryInDBBase):
    """Properties to return to client"""

    pass


class ReactionEntryInDB(ReactionEntryInDBBase):
    """Properties stored in DB"""

    pass
