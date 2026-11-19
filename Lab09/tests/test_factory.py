"""Section 3 + 7: Factory pattern tests."""
import unittest
from pathlib import Path

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory

PROJECT_FOLDER = Path(__file__).resolve().parent.parent


class TestProductFactory(unittest.TestCase):

    def setUp(self):
        """Runs before EVERY test: a fresh supplier each time."""
        self.supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.0, 10,
                                        self.supplier, 1.2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)          # still a Product (LSP)
        self.assertEqual(product.get_weight(), 1.2)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.9, 100,
                                        self.supplier, 350.0)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 350.0)

    def test_extra_value_defaults_to_zero(self):
        product = ProductFactory.create("physical", "P002", "Chair", 80.0, 3, self.supplier)
        self.assertEqual(product.get_weight(), 0.0)

    def test_unknown_type_raises_clear_value_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_client_code_does_not_construct_products_directly(self):
        """Design check: only the factory calls the concrete constructors."""
        for filename in ["inventory_manager.py", "file_handler.py"]:
            source = (PROJECT_FOLDER / filename).read_text()
            self.assertNotIn("PhysicalProduct(", source, filename)
            self.assertNotIn("DigitalProduct(", source, filename)


if __name__ == "__main__":
    unittest.main()
