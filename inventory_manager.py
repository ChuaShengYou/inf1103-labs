import json

# Global Constant
INVENTORY_FILE = "inventory.json"


def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:
            inventory = json.load(file)
        print(f"{INVENTORY_FILE} found.")
        print("Inventory loaded successfully.")
    except FileNotFoundError:
        inventory = []
        print(f"{INVENTORY_FILE} not found. Starting with empty inventory.")

    return inventory


def save_inventory(inventory):
    print("Saving inventory...")
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)

    print(f"Inventory saved successfully to {INVENTORY_FILE}.")


def display_all(inventory):
    if not inventory:
        print("Inventory is empty.")
        return

    print("\nCurrent Inventory")
    print("-" * 48)
    for product in inventory:
        print(
            f'ID: {product["id"]} | '
            f'Name: {product["name"]} | '
            f'Price: ${product["price"]:.2f} | '
            f'Stock: {product["stock"]}'
        )
    print("-" * 48)


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    product_name = input("Product Name: ").strip()

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid price or stock quantity. Product not added.")
        return

    new_product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }

    inventory.append(new_product)

    print("\nProduct added successfully!")


def search_product(inventory, product_id):
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print(f'Name: {product["name"]}')
    print(f'Current Stock: {product["stock"]}')

    try:
        new_stock = int(input("New Stock Quantity: "))
    except ValueError:
        print("Invalid stock quantity. Stock not updated.")
        return

    product["stock"] = new_stock
    print("\nStock updated successfully!")


def handle_search(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    print(f'ID: {product["id"]}')
    print(f'Name: {product["name"]}')
    print(f'Price: ${product["price"]:.2f}')
    print(f'Stock: {product["stock"]}')
    print("-" * 48)


def main():
    inventory = load_inventory()

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")

        option = input("Enter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            handle_search(inventory)
        elif option == "5":
            save_inventory(inventory)
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
