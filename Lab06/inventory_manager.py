from product import Product
from file_handler import load_inventory, save_inventory

# Global Constant
INVENTORY_FILE = "inventory.json"

def handle_add(inventory):
    print("\nAdd New Product")
    product_id = input("Enter Product ID: ").strip()
    product_name = input("Enter Product Name: ").strip()

    try:
        price = float(input("Price:"))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid price or stock quantity. Product not added.")
        return

    new_product = Product(product_id, product_name, price, stock)
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
    print(f"ID: {product.get_product_id()}")
    print(f"Name: {product.get_name()}")
    print(f"Price: ${product.get_price():.2f}")
    print(f"Stock: {product.get_stock()}")
    print("-" * 48)


def main():
    inventory = load_inventory(INVENTORY_FILE)

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