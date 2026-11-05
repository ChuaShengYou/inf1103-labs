from product import Product

class DigitalProduct(Product):
    PRODUCT_TYPE = "digital"

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["download_size"] = self.__download_size
        return data

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via a download link."
    
    def display_information(self):
        print(
            f"ID: {self.get_product_id()} | "
            f"Name: {self.get_name()} | "
            f"Price: ${self.get_price():.2f} | "
            f"Stock: {self.get_stock()} | "
            f"Download Size: {self.__download_size:.2f} MB"
        )