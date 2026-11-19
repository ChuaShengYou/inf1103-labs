from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


class ProductFactory:
    """The ONE place that decides which Product subclass to build."""

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, extra_value: float = 0.0) -> Product:
        """Return a new Product.

        extra_value is the weight (kg) for a physical product, or the
        download size (MB) for a digital product. It defaults to 0.0
        because products.csv has no column for it.
        """
        if product_type == PhysicalProduct.PRODUCT_TYPE:        # "physical"
            return PhysicalProduct(product_id, name, price, stock, supplier, extra_value)
        elif product_type == DigitalProduct.PRODUCT_TYPE:       # "digital"
            return DigitalProduct(product_id, name, price, stock, supplier, extra_value)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
