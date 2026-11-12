from product import Product


class Inventory:
    """A whole that groups Product objects (aggregation). It never creates or destroys them."""

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def remove_product(self, product_id: str) -> bool:
        """Remove the reference only. Return True if removed, False if not found."""
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all_products(self) -> None:
        if not self.__products:
            print("Inventory is empty.")
            return

        print("\nCurrent Inventory")
        print("-" * 48)
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    def get_products(self) -> list[Product]:
        """Return a copy, so other code cannot change the inventory's own list."""
        return list(self.__products)