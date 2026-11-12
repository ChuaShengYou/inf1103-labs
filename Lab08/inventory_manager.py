from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order
from file_handler import load_inventory, save_inventory

# Global Constant
INVENTORY_FILE = "inventory.json"


def find_supplier(inventory: Inventory, supplier_id: str) -> Supplier | None:
    """Return an existing Supplier already used by a product, or None."""
    for product in inventory.get_products():
        supplier = product.get_supplier()
        if supplier.get_supplier_id() == supplier_id:
            return supplier
    return None


def ask_for_supplier(inventory: Inventory) -> Supplier:
    """Reuse an existing Supplier object if the ID is known, otherwise create a new one."""
    supplier_id = input("Supplier ID: ").strip()
    supplier = find_supplier(inventory, supplier_id)
    if supplier is not None:
        print(f"Using existing supplier: {supplier.get_name()}")
        return supplier

    name = input("Supplier Name: ").strip()
    email = input("Supplier Email: ").strip()
    return Supplier(supplier_id, name, email)


def handle_add(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Choose product type: ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type. Product not added.")
        return

    product_id = input("Enter Product ID: ").strip()
    if inventory.find_product(product_id) is not None:
        print("A product with this ID already exists. Product not added.")
        return
    product_name = input("Enter Product Name: ").strip()

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if product_type == "1":
            extra_value = float(input("Weight (kg): "))
        else:
            extra_value = float(input("Download Size (MB): "))
    except ValueError:
        print("Invalid number entered. Product not added.")
        return

    supplier = ask_for_supplier(inventory)

    new_product: Product
    try:
        if product_type == "1":
            new_product = PhysicalProduct(product_id, product_name, price, stock,
                                          supplier, extra_value)
        else:
            new_product = DigitalProduct(product_id, product_name, price, stock,
                                         supplier, extra_value)
    except ValueError as error:
        print(f"Error: {error} Product not added.")
        return

    inventory.add_product(new_product)
    print("\nProduct added successfully!")


def handle_update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter product ID: ").strip()
    product = inventory.find_product(product_id)

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


def handle_search(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter product ID: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print("-" * 60)
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("Supplied by:")
    product.get_supplier().display_information()
    print("-" * 60)


def handle_remove(inventory: Inventory) -> None:
    print("\nRemove Product")
    product_id = input("Enter product ID: ").strip()
    if inventory.remove_product(product_id):
        print("Product removed from the inventory.")
    else:
        print("Product not found.")


def handle_create_order(inventory: Inventory) -> None:
    print("\nCreate Order")
    order_id = input("Enter Order ID: ").strip()
    order = Order(order_id)

    while True:
        product_id = input("Product ID to add (press Enter to finish): ").strip()
        if product_id == "":
            break

        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue

        try:
            quantity = int(input("Quantity: "))
        except ValueError:
            print("Quantity must be a whole number. Line not added.")
            continue

        try:
            order.add_order_line(product, quantity)   # the Order creates the OrderLine
        except ValueError as error:
            print(f"Error: {error} Line not added.")
            continue
        print("Line added.")

    order.display_order()


def main() -> None:
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
        print("5. Remove Product")
        print("6. Create Order")
        print("7. Save Inventory")
        print("8. Exit")
        print("----------------------------")

        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all_products()
        elif option == "2":
            handle_add(inventory)
        elif option == "3":
            handle_update_stock(inventory)
        elif option == "4":
            handle_search(inventory)
        elif option == "5":
            handle_remove(inventory)
        elif option == "6":
            handle_create_order(inventory)
        elif option == "7":
            save_inventory(inventory, INVENTORY_FILE)
        elif option == "8":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, INVENTORY_FILE)
            print("\nThank you for using the Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()