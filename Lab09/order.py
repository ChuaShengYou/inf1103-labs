from order_line import OrderLine
from product import Product
from discount_strategy import DiscountStrategy, NoDiscount


class Order:
    """A customer order. It creates, owns and removes its own OrderLine objects (composition).
    It USES a DiscountStrategy (association) but never decides how the discount works."""

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        if discount is None:            # no strategy given -> use the default
            discount = NoDiscount()
        self.__discount: DiscountStrategy = discount

    def get_order_id(self) -> str:
        return self.__order_id

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Swap the strategy at runtime."""
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)   # the Order creates its own part
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the line for this product. Return True if removed, False if not found."""
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        """Read-only view. A tuple has no append(), so lines cannot be added from outside."""
        return tuple(self.__order_lines)

    def calculate_subtotal(self) -> float:
        """Total BEFORE the discount."""
        return round(sum(line.calculate_subtotal() for line in self.__order_lines), 2)

    def calculate_total(self) -> float:
        """Total AFTER the discount. No if/elif about discount types here."""
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return round(self.__discount.apply(total), 2)

    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("-" * 60)
        if not self.__order_lines:
            print("No order lines.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("-" * 60)
        subtotal = self.calculate_subtotal()
        total = self.calculate_total()
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Discount: -${subtotal - total:.2f} ({type(self.__discount).__name__})")
        print(f"Total: ${total:.2f}")
