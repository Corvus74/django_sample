from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict
from django.contrib.auth import get_user_model

from .dependencies import get_replacement_part_service, CommonQueryParams, get_current_user # Import the new dependency
from .schemas import ReplacementPart, ReplacementPartCreate
from .services import ReplacementPartService

User = get_user_model()
router = APIRouter()


@router.get("/replacement-parts", response_model=List[ReplacementPart], tags=["Replacement Parts"])
def get_replacement_parts(
    service: ReplacementPartService = Depends(get_replacement_part_service),
):
    """Endpoint to retrieve a list of replacement parts. This is a public endpoint."""
    return service.get_replacement_parts()


@router.post("/replacement-parts/", response_model=ReplacementPart, status_code=status.HTTP_201_CREATED, tags=["Replacement Parts"])
def add_replacement_part(
    part: ReplacementPartCreate,
    service: ReplacementPartService = Depends(get_replacement_part_service),
    current_user: User = Depends(get_current_user), # Secure this endpoint
):
    """Endpoint to add a new replacement part. Requires authentication."""
    # You can optionally use the user, e.g., for logging: print(f"User {current_user.username} is adding a part.")
    return service.add_replacement_part(part)


@router.delete("/replacement-parts/{part_id}", status_code=status.HTTP_200_OK, tags=["Replacement Parts"])
def remove_replacement_part(
    part_id: int,
    service: ReplacementPartService = Depends(get_replacement_part_service),
    current_user: User = Depends(get_current_user), # Secure this endpoint
):
    """Endpoint to remove a replacement part by ID. Requires authentication."""
    removed_part = service.remove_replacement_part(part_id)
    if not removed_part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Replacement part not found")
    return {"message": f"Replacement part with ID {part_id} removed successfully"}


@router.get("/items/", tags=["Items"])
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    """This is a public endpoint."""
    return {
        "message": "Here are your items!",
        "params": commons,
    }


@router.get("/users/me", tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    """A test endpoint to check the current authenticated user."""
    return {"username": current_user.username, "email": current_user.email}
