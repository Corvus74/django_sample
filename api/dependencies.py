from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist

from .services import ReplacementPartService
from .repositories import ReplacementPartRepository

# --- User and Session Dependencies ---

User = get_user_model()

async def get_current_user(request: Request) -> User:
    """
    A FastAPI dependency that checks for a valid Django session cookie
    and returns the authenticated user. If the user is not authenticated,
    it raises an HTTP 401 Unauthorized error.
    """
    session_key = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if not session_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        session = Session.objects.get(session_key=session_key)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        user = User.objects.get(pk=user_id)
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User inactive or deleted",
            )
        return user
    except (ObjectDoesNotExist, User.DoesNotExist):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session",
        )


# --- Service and Repository Dependencies ---

# Create a single instance of the repository at module level
_replacement_part_repository_instance = ReplacementPartRepository()

# Create a single instance of the service, injecting the repository
_replacement_part_service_instance = ReplacementPartService(repository=_replacement_part_repository_instance)

def get_replacement_part_service() -> ReplacementPartService:
    # Return the single instance of the service
    return _replacement_part_service_instance


class CommonQueryParams(BaseModel):
    """A dependency to extract common query parameters with validation."""
    q: Optional[str] = None
    skip: int = Field(0, ge=0, description="Number of items to skip, must be non-negative")
    limit: int = Field(100, ge=0, description="Maximum number of items to return, must be non-negative")
