"""Section 2 + 7: Strategy pattern tests."""
import ast
import inspect
import textwrap
import unittest

from supplier import Supplier
from product_factory import ProductFactory
from order import Order
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)


def make_order_totalling_250(discount: DiscountStrategy | None = None) -> Order:
    """Helper: an order whose lines add up to exactly 250."""
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, supplier)
    order = Order("O001", discount)
    order.add_order_line(lamp, 10)          # 10 x 25.00 = 250.00
    return order


class TestStrategies(unittest.TestCase):
    """Each strategy on its own."""

    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount_takes_percent_off(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225.0)

    def test_bulk_discount_at_or_above_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)   # boundary: 200 counts

    def test_bulk_discount_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(199.99), 199.99)

    def test_student_discount_is_five_percent(self):
        self.assertAlmostEqual(StudentDiscount().apply(250), 237.5)

    def test_discount_strategy_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_invalid_percentage_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)


class TestOrderUsesStrategy(unittest.TestCase):
    """Order delegates to whatever strategy it holds."""

    def test_default_is_no_discount(self):
        order = make_order_totalling_250()
        self.assertIsInstance(order.get_discount(), NoDiscount)
        self.assertEqual(order.calculate_total(), 250.0)

    def test_predict_first_bulk_then_percentage(self):
        order = make_order_totalling_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))      # same order, new strategy
        self.assertEqual(order.calculate_total(), 225.0)

    def test_new_strategy_needs_no_change_to_order(self):
        class HalfPrice(DiscountStrategy):              # brand-new strategy, defined here
            def apply(self, total: float) -> float:
                return total / 2
        order = make_order_totalling_250(HalfPrice())
        self.assertEqual(order.calculate_total(), 125.0)

    def test_two_orders_can_share_one_strategy_object(self):
        shared = PercentageDiscount(10)
        order_a = make_order_totalling_250(shared)
        order_b = make_order_totalling_250(shared)
        self.assertIs(order_a.get_discount(), order_b.get_discount())

    def test_calculate_total_has_no_if_elif(self):
        """Design check: the discount decision is NOT inside Order."""
        source = textwrap.dedent(inspect.getsource(Order.calculate_total))
        tree = ast.parse(source)     # real code structure, so comments/docstrings are ignored
        if_nodes = [node for node in ast.walk(tree) if isinstance(node, (ast.If, ast.IfExp))]
        self.assertEqual(if_nodes, [])


if __name__ == "__main__":
    unittest.main()
