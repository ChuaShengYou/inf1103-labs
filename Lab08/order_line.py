from product import Product

class OrderLine:
    """One product and quantity inside an Order. Only Order should create it (composition)."""
    def __init__(self, product: Product, quantity: int)-> None:
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(
            f"{self.__product.get_product_id()} | "
            f"{self.__product.get_name()} | "
            f"{self.__quantity} x ${self.__product.get_price():.2f} = "
            f"${self.calculate_subtotal():.2f}"
        )