from django.test import TestCase
from .models import ReplacementPart

class ReplacementPartModelTest(TestCase):
    """Tests for the ReplacementPart model."""

    def test_create_replacement_part(self):
        """Test that a ReplacementPart can be created successfully."""
        part = ReplacementPart.objects.create(
            name="Test Part",
            sku="SKU-TEST-123",
            quantity=50
        )
        self.assertEqual(part.name, "Test Part")
        self.assertEqual(part.sku, "SKU-TEST-123")
        self.assertEqual(part.quantity, 50)
        self.assertIsInstance(part.id, int)
        print(f"Successfully created and tested part: {part.name}")

    def test_get_all_replacement_parts(self):
        """Test retrieving all replacement parts."""
        ReplacementPart.objects.create(name="Part A", sku="A01", quantity=10)
        ReplacementPart.objects.create(name="Part B", sku="B02", quantity=20)
        
        all_parts = ReplacementPart.objects.all()
        self.assertEqual(all_parts.count(), 2)
        print(f"Successfully retrieved {all_parts.count()} parts.")
