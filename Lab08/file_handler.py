import json

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory


def get_or_create_supplier(data: dict, suppliers: dict[str, Supplier]) -> Supplier:
    """Return the Supplier with this ID, creating it only the first time it is seen.

    This way, two products from the same supplier share ONE Supplier object,
    just like they did before the program was closed.
    """
    supplier_id = data["supplier_id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data["name"], data["contact_email"])
    return suppliers[supplier_id]


def create_product(item: dict, suppliers: dict[str, Supplier]) -> Product:
    """Turn one JSON dictionary into the correct Product subclass object."""
    product_type = item["type"]
    supplier = get_or_create_supplier(item["supplier"], suppliers)

    if product_type == PhysicalProduct.PRODUCT_TYPE:
        return PhysicalProduct(
            item["id"], item["name"], item["price"], item["stock"],
            supplier, item["weight"]
        )
    if product_type == DigitalProduct.PRODUCT_TYPE:
        return DigitalProduct(
            item["id"], item["name"], item["price"], item["stock"],
            supplier, item["download_size"]
        )

    raise ValueError(f"Unknown product type '{product_type}'.")


def load_inventory(filename: str) -> Inventory:
    inventory = Inventory()

    try:
        with open(filename, "r") as file:
            data = json.load(file)
        print(f"{filename} found.")
    except FileNotFoundError:
        print(f"{filename} not found. Starting with empty inventory.")
        return inventory

    suppliers: dict[str, Supplier] = {}
    for item in data:
        inventory.add_product(create_product(item, suppliers))

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory, filename: str) -> None:
    print("Saving inventory...")

    data = []
    for product in inventory.get_products():
        data.append(product.to_dict())

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Inventory saved successfully to {filename}.")