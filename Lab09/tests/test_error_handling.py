"""Section 5 + 7: exception handling tests (user input retry and CSV loading)."""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from supplier import Supplier
from inventory import Inventory
from file_handler import load_products
from inventory_manager import get_positive_float

CSV_TEXT = (
    "product_type,product_id,name,price,stock_quantity\n"
    "physical,P001,Desk Lamp,25.00,10\n"
    "digital,D001,Photo Editor,49.90,100\n"
    "service,S001,Installation,30.00,5\n"
    "physical,P002,Office Chair,abc,3\n"
    "physical,P003,Monitor Stand,39.50,7\n"
)


class TestGetPositiveFloat(unittest.TestCase):

    def test_retries_until_valid(self):
        # patch() replaces input() so the test can "type" abc, -5, 12.50 for us
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            output = io.StringIO()
            with redirect_stdout(output):
                value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_is_not_positive(self):
        with patch("builtins.input", side_effect=["0", "1"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(get_positive_float("Price: "), 1.0)


class TestLoadProducts(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
        self.inventory = Inventory()
        self.folder = tempfile.TemporaryDirectory()        # deleted again in tearDown
        self.csv_path = os.path.join(self.folder.name, "products.csv")
        with open(self.csv_path, "w", newline="") as file:
            file.write(CSV_TEXT)

    def tearDown(self):
        self.folder.cleanup()

    def run_load(self, path: str) -> list[str]:
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue().splitlines()

    def test_valid_rows_load_and_bad_rows_are_skipped(self):
        lines = self.run_load(self.csv_path)
        loaded_ids = [p.get_product_id() for p in self.inventory.get_products()]
        self.assertEqual(loaded_ids, ["P001", "D001", "P003"])
        self.assertEqual(lines, [
            "Skipping row 4 (service,S001,Installation,30.00,5): Unknown product type: service",
            "Skipping row 5 (physical,P002,Office Chair,abc,3): could not convert string to float: 'abc'",
            "3 products loaded.",
            "Load attempt finished.",
        ])

    def test_missing_file_is_handled(self):
        lines = self.run_load(os.path.join(self.folder.name, "missing.csv"))
        self.assertEqual(len(self.inventory.get_products()), 0)
        self.assertEqual(lines[-1], "Load attempt finished.")
        self.assertTrue(lines[0].startswith("Products file not found:"))
        self.assertNotIn("products loaded", " ".join(lines))   # else block did NOT run

    def test_loading_twice_skips_duplicates(self):
        self.run_load(self.csv_path)
        lines = self.run_load(self.csv_path)
        self.assertIn("0 products loaded.", lines)
        self.assertEqual(len(self.inventory.get_products()), 3)


if __name__ == "__main__":
    unittest.main()
