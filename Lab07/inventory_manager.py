import os

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from file_handler import load_inventory, save_inventory

# Global Constant
# Always use the inventory.json next to this script, no matter where it is run from
INVENTORY_FILE = "inventory.json"

def handle_add(inventory):
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Choose product type: ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type. Product not added.")
        return
    
    product_id = input("Enter Product ID: ").strip()
    product_name = input("Enter Product Name: ").strip()

    try:
        price = float(input("Price:"))
        stock = int(input("Stock Quantity: "))
        if product_type == "1":
            extra_value = float(input("Weight (kg): "))
        else:
            extra_value = float(input("Download Size (MB): "))
    except ValueError:
        print("Invalid number entered. Product not added.")
        return

    try:
        if product_type == "1":
            new_product = PhysicalProduct(product_id, product_name, price, stock, extra_value)
        else:
            new_product = DigitalProduct(product_id, product_name, price, stock, extra_value)
    except ValueError as error:
        print(f"Error: {error}. Product not added.")
        return
    
    inventory.add_product(new_product)
    print("\nProduct added successfully!")

def handle_update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    try:
        new_stock = int(input("New Stock Quantity: "))
    except ValueError:
        print("Invalid stock quantity. Stock not updated.")
        return

    if product.update_stock(new_stock):
        print("Stock updated successfully!")
    else:
        print("Stock cannot be negative. Stock not updated.")

def handle_search(inventory):
    print("\nSearch Product")
    product_id = input("Enter product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print("-" * 48)
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("-" * 48)


def main():
    try:
        inventory = load_inventory(INVENTORY_FILE)
    except KeyError as error:
        print(f"Error: a product in {INVENTORY_FILE} is missing the field {error}.")
        print("Program stopped so that your data file is not overwritten.")
        return
    except ValueError as error:
        print(f"Error: {INVENTORY_FILE} contains invalid data: {error}")
        print("Program stopped so that your data file is not overwritten.")
        return

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
            inventory.display_all()
        elif option == "2":
            handle_add(inventory)
        elif option == "3":
            handle_update_stock(inventory)
        elif option == "4":
            handle_search(inventory)
        elif option == "5":
            save_inventory(inventory, INVENTORY_FILE)
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, INVENTORY_FILE)
            print("\nThank you for using the Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()