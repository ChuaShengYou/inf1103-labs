from product import Product
from supplier import Supplier

class DigitalProduct(Product):
    PRODUCT_TYPE = "digital"

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size: float= download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["download_size"] = self.__download_size
        return data

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via a download link."
    
    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Digital | Download Size: {self.__download_size:.2f} MB")
