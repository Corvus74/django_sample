from typing import List, Optional

from api.repositories import ReplacementPartRepository
from api.schemas import ReplacementPart as PydanticReplacementPart, ReplacementPartCreate
from api.mappers import to_pydantic_replacement_part


class ReplacementPartService:
    """
    A service to manage replacement parts.
    This contains the business logic and uses a repository for data access.
    """

    def __init__(self, repository: ReplacementPartRepository):
        self.repository = repository

    def get_replacement_parts(self) -> List[PydanticReplacementPart]:
        """Retrieve all replacement parts."""
        django_parts = self.repository.get_all()
        return [to_pydantic_replacement_part(part) for part in django_parts]

    def add_replacement_part(self, part_create: ReplacementPartCreate) -> PydanticReplacementPart:
        """Create a new replacement part."""
        django_part = self.repository.create(part_create)
        return to_pydantic_replacement_part(django_part)

    def remove_replacement_part(self, part_id: int) -> Optional[PydanticReplacementPart]:
        """Remove a replacement part by its ID."""
        django_part = self.repository.delete_by_id(part_id)
        if django_part:
            return to_pydantic_replacement_part(django_part)
        return None
