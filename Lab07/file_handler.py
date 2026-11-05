import json

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

def create_product(item):
    """Turn one JSON dictionary into the correct Product subclass object."""
    product_type = item["type"]

    if product_type == PhysicalProduct.PRODUCT_TYPE:
        return PhysicalProduct(
            item["id"], item["name"], item["price"], item["stock"], item["weight"]
        )
    if product_type == DigitalProduct.PRODUCT_TYPE:
        return DigitalProduct(
            item["id"], item["name"], item["price"], item["stock"], item["download_size"]
        )

    raise ValueError(f"Unknown product type '{product_type}'.")

def load_inventory(filename):
    inventory = Inventory()

    try:
        with open(filename, "r") as file:
            data = json.load(file)
        print(f"{filename} found.")
    except FileNotFoundError:
        print(f"{filename} not found. Starting with empty inventory.")
        return inventory

    for item in data:
        inventory.add_product(create_product(item))

    print("Inventory loaded successfully.")
    return inventory
    
def save_inventory(inventory, filename):
    print("Saving inventory...")

    data = []
    for product in inventory.get_products():
        data.append(product.to_dict())

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Inventory saved successfully to {filename}.")