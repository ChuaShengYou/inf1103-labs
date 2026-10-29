import json

from product import Product 
from inventory import Inventory

def load_inventory(filename):
    inventory = Inventory()

    try:
        with open(filename, "r") as file:
            data = json.load(file)
        print(f"{filename} found.")
        print("Inventory loaded successfully.")
    except FileNotFoundError:
        print(f"{filename} not found. Starting with empty inventory.")
        return inventory

    for item in data:
        product = Product(item["id"], item["name"], item["price"], item["stock"])
        inventory.add_product(product)
    
    return inventory

def save_inventory(inventory, filename):
    print("Saving inventory...")

    data = []
    for product in inventory.get_products():
        data.append(product.to_dict())

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Inventory saved successfully to {filename}.")