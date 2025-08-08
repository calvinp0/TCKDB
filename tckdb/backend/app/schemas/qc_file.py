"""Schemas for QCFile model."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class QCFileBase(BaseModel):
    calc_type: str = Field(..., title="Calculation type")
    status: str = Field(..., title="Status of the calculation")
    level_id: int = Field(..., title="Level of theory ID")
    ess_id: int = Field(..., title="Electronic structure software ID")
    input_name: Optional[str] = Field(None, title="Input file name")
    output_name: Optional[str] = Field(None, title="Output file name")
    compressed: bool = Field(True, title="Are files compressed")
    checksum: str = Field(..., title="Checksum of stored files")


class QCFileCreate(QCFileBase):
    species_id: Optional[int] = None
    transition_state_id: Optional[int] = None
    np_species_id: Optional[int] = None
    input_file: Optional[bytes] = None
    output_file: Optional[bytes] = None


class QCFile(QCFileBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
