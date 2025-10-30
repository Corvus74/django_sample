from pydantic import BaseModel, Field


class ReplacementPartBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the replacement part")
    sku: str = Field(..., alias="stockKeepingUnit", min_length=1, description="Stock Keeping Unit, must be unique")
    quantity: int = Field(..., ge=0, description="Quantity of the replacement part, must be non-negative")

    class Config:
        populate_by_name = True # Allows using alias for field names


class ReplacementPartCreate(ReplacementPartBase):
    # This schema is used for creating new parts (POST requests)
    # ID is not expected on creation
    pass


class ReplacementPart(ReplacementPartBase):
    # This schema is used for responses (GET, POST response, etc.)
    # ID is expected to be present after creation
    id: int = Field(..., description="Unique identifier of the replacement part")


# Note: List is not a schema itself, but a type hint for lists of schemas
# from typing import List
