from supplier import Supplier
from product_factory import ProductFactory
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)
from file_handler import load_inventory, save_inventory, load_products

# Global Constants
INVENTORY_FILE = "inventory.json"
PRODUCTS_FILE = "products.csv"


# ---------------------------------------------------------------
# Input helpers (Lab 9 Section 5.1): keep asking until valid
# ---------------------------------------------------------------
def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter zero or a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 2.5")


def get_non_negative_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter zero or a positive whole number.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 10")


# ---------------------------------------------------------------
# Supplier helpers (unchanged from Lab 8)
# ---------------------------------------------------------------
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


# ---------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------
def handle_add(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    choice = input("Choose product type: ").strip()

    if choice == "1":
        product_type = "physical"
        extra_prompt = "Weight (kg): "
    elif choice == "2":
        product_type = "digital"
        extra_prompt = "Download Size (MB): "
    else:
        print("Invalid product type. Product not added.")
        return

    product_id = input("Enter Product ID: ").strip()
    if inventory.find_product(product_id) is not None:
        print("A product with this ID already exists. Product not added.")
        return
    product_name = input("Enter Product Name: ").strip()

    price = get_positive_float("Price: ")                  # retries until > 0
    stock = get_non_negative_int("Stock Quantity: ")       # retries until >= 0
    extra_value = get_non_negative_float(extra_prompt)     # retries until >= 0

    supplier = ask_for_supplier(inventory)

    try:
        new_product = ProductFactory.create(product_type, product_id, product_name,
                                            price, stock, supplier, extra_value)
        inventory.add_product(new_product)
    except ValueError as error:
        print(f"Error: {error} Product not added.")
        return

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


def choose_discount() -> DiscountStrategy:
    """Menu code picks WHICH strategy object to create. Order never sees this if/elif."""
    print("\nDiscount options")
    print("1. No discount")
    print("2. 10% off")
    print("3. $20 off orders of $200 or more")
    print("4. Student discount (5% off)")
    while True:
        choice = input("Choose discount: ").strip()
        if choice == "1":
            return NoDiscount()
        elif choice == "2":
            return PercentageDiscount(10)
        elif choice == "3":
            return BulkDiscount(200, 20)
        elif choice == "4":
            return StudentDiscount()
        print("Please choose 1, 2, 3 or 4.")


def handle_create_order(inventory: Inventory) -> None:
    print("\nCreate Order")
    order_id = input("Enter Order ID: ").strip()
    order = Order(order_id)                 # starts with NoDiscount()

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
            order.add_order_line(product, quantity)   # OrderLine validates quantity > 0
        except ValueError as error:
            print(f"Error: {error} Line not added.")
            continue
        print("Line added.")

    order.set_discount(choose_discount())   # swap the strategy at runtime
    order.display_order()


def handle_load_products(inventory: Inventory) -> None:
    print("\nLoad Products from CSV")
    path = input(f"CSV file (press Enter for {PRODUCTS_FILE}): ").strip() or PRODUCTS_FILE
    print("Which supplier supplies these products?")
    supplier = ask_for_supplier(inventory)
    load_products(path, inventory, supplier)


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
        print("8. Load Products from CSV")
        print("9. Exit")
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
            handle_load_products(inventory)
        elif option == "9":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, INVENTORY_FILE)
            print("\nThank you for using the Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
