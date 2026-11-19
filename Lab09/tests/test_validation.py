"""Section 4 + 7: validation tests (invalid data is rejected by the class that owns the rule)."""
import unittest

from supplier import Supplier
from product_factory import ProductFactory
from inventory import Inventory
from order import Order


class TestProductValidation(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")

    def test_zero_price_rejected(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("physical", "P001", "Lamp", 0, 10, self.supplier)
        self.assertEqual(str(context.exception), "Price must be greater than zero.")

    def test_negative_price_rejected_for_digital_too(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "App", -5, 10, self.supplier)

    def test_negative_stock_rejected(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("physical", "P001", "Lamp", 25.0, -1, self.supplier)
        self.assertEqual(str(context.exception), "Stock quantity cannot be negative.")

    def test_zero_stock_allowed(self):
        product = ProductFactory.create("digital", "D001", "App", 9.9, 0, self.supplier)
        self.assertEqual(product.get_stock(), 0)

    def test_update_stock_still_refuses_negative(self):
        product = ProductFactory.create("digital", "D001", "App", 9.9, 5, self.supplier)
        self.assertFalse(product.update_stock(-1))
        self.assertEqual(product.get_stock(), 5)

    def test_duplicate_id_rejected_by_inventory(self):
        inventory = Inventory()
        inventory.add_product(ProductFactory.create("physical", "P001", "Lamp", 25.0, 1, self.supplier))
        with self.assertRaises(ValueError):
            inventory.add_product(ProductFactory.create("digital", "P001", "App", 9.9, 1, self.supplier))


class TestOrderLineValidation(unittest.TestCase):

    def setUp(self):
        supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
        self.lamp = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10, supplier)
        self.order = Order("O001")

    def test_zero_quantity_rejected(self):
        with self.assertRaises(ValueError) as context:
            self.order.add_order_line(self.lamp, 0)
        self.assertEqual(str(context.exception), "Quantity must be greater than zero.")

    def test_negative_quantity_rejected(self):
        with self.assertRaises(ValueError):
            self.order.add_order_line(self.lamp, -3)

    def test_rejected_line_is_not_added(self):
        try:
            self.order.add_order_line(self.lamp, 0)
        except ValueError:
            pass
        self.assertEqual(len(self.order.get_order_lines()), 0)


if __name__ == "__main__":
    unittest.main()
