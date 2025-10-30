from api.models import ReplacementPart as DjangoReplacementPart
from api.schemas import ReplacementPart as PydanticReplacementPart

def to_pydantic_replacement_part(django_part: DjangoReplacementPart) -> PydanticReplacementPart:
    """Converts a Django ORM ReplacementPart instance to a Pydantic ReplacementPart schema."""
    return PydanticReplacementPart(
        id=django_part.id,
        name=django_part.name,
        sku=django_part.sku,
        quantity=django_part.quantity
    )
