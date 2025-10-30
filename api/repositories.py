from typing import List, Optional
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from api.models import ReplacementPart as DjangoReplacementPart
from api.schemas import ReplacementPartCreate


class ReplacementPartRepository:
    """Encapsulates all data access logic for Replacement Parts."""

    def get_all(self) -> List[DjangoReplacementPart]:
        """Retrieve all replacement parts from the database."""
        return DjangoReplacementPart.objects.all()

    def create(self, part_create: ReplacementPartCreate) -> DjangoReplacementPart:
        """Create and save a new replacement part in the database."""
        with transaction.atomic():
            return DjangoReplacementPart.objects.create(
                name=part_create.name,
                sku=part_create.sku,
                quantity=part_create.quantity
            )

    def delete_by_id(self, part_id: int) -> Optional[DjangoReplacementPart]:
        """Delete a replacement part by its ID."""
        with transaction.atomic():
            try:
                part_to_delete = DjangoReplacementPart.objects.get(id=part_id)
                part_to_delete.delete()
                return part_to_delete # Return the object that was deleted
            except ObjectDoesNotExist:
                return None
