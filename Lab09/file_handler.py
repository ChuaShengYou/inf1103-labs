import csv
import json

from supplier import Supplier
from product import Product
from product_factory import ProductFactory
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
    """Turn one JSON dictionary into the correct Product subclass object (via the factory)."""
    supplier = get_or_create_supplier(item["supplier"], suppliers)
    # The JSON file stores the extra value under a type-specific key.
    extra_value = item.get("weight", item.get("download_size", 0.0))
    return ProductFactory.create(item["type"], item["id"], item["name"], item["price"],
                                 item["stock"], supplier, extra_value)


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


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Lab 9 Section 5.2: load products from a CSV file, skipping bad rows."""
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)                      # skip the header row
            for row_number, row in enumerate(reader, start=2):
                if not row:                         # ignore completely blank lines
                    continue
                try:
                    product_type, product_id, name, price_text, stock_text = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price_text), int(stock_text),
                                                    supplier)
                    inventory.add_product(product)
                except ValueError as error:
                    print(f"Skipping row {row_number} ({','.join(row)}): {error}")
                else:
                    loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
