from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier

class PhysicalProduct(Product, CanBeShipped):
    """A product that has a weight and must be shipped."""

    BASE_SHIPPING_FEE = 5.00      # dollars, charged on every shipment
    SHIPPING_RATE_PER_KG = 2.00   # dollars for each kilogram
    PRODUCT_TYPE = "physical"

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["weight"] = self.__weight
        return data

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        cost = self.BASE_SHIPPING_FEE + self.SHIPPING_RATE_PER_KG * self.__weight
        return round(cost, 2)