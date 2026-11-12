"""Lab 8 tests: association, aggregation, composition, LSP and polymorphism.

Run with:  python lab8_tests.py
"""
import os
import tempfile

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from file_handler import load_inventory, save_inventory

passed = 0
failed = 0


def check(description: str, condition: bool) -> None:
    """Print PASS or FAIL for one requirement and count the result."""
    global passed, failed
    if condition:
        passed += 1
        print(f"PASS: {description}")
    else:
        failed += 1
        print(f"FAIL: {description}")


def show_product_details(product: Product) -> None:
    """Lab 8 section 6.2: works with ANY Product, without checking its subclass."""
    product.display_information()
    print(product.get_fulfilment_info())


# ------------------------------------------------------------------
print("=== Section 2: Association (Supplier and Product) ===")
supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.0, 15, supplier, 2.5)
antivirus = DigitalProduct("D001", "Antivirus Software", 49.9, 100, supplier, 350.0)

laptop.get_supplier().display_information()
antivirus.get_supplier().display_information()

check("Product stores a reference to the Supplier object", laptop.get_supplier() is supplier)
check("Both products refer to the SAME Supplier object",
      laptop.get_supplier() is antivirus.get_supplier())
check("The supplier attribute holds a Supplier object (not just a name or ID)",
      isinstance(laptop.get_supplier(), Supplier))

print("\nPredict first: del supplier")
del supplier                    # removes the NAME 'supplier', not the object
laptop.get_supplier().display_information()
antivirus.get_supplier().display_information()
check("Products still reach their Supplier after 'del supplier'",
      laptop.get_supplier().get_name() == "TechSource Pte Ltd")

# A Product can also keep working if its supplier variable is never used again,
# and a Supplier can exist with no products at all:
lonely_supplier = Supplier("S999", "New Supplier", "hello@new.example.com")
check("A Supplier can exist without any Product", lonely_supplier.get_name() == "New Supplier")

# ------------------------------------------------------------------
print("\n=== Section 3: Aggregation (Inventory and Product) ===")
supplier2 = Supplier("S002", "SoftWorks Digital", "orders@softworks.example.com")
mouse = PhysicalProduct("P002", "Mouse", 25.5, 60, supplier2, 0.1)   # 1. created FIRST
inventory_a = Inventory()
inventory_b = Inventory()

inventory_a.add_product(mouse)                                        # 2. add to A
check("Product added to Inventory A", inventory_a.find_product("P002") is mouse)

print("\nPredict first: does the Product still work after removal from A?")
removed = inventory_a.remove_product("P002")                          # 3. remove from A
check("remove_product() returns True for an existing product", removed)
check("Inventory A no longer contains the product", inventory_a.find_product("P002") is None)
mouse.display_information()                                           # still works
check("The Product object still works after removal", mouse.get_name() == "Mouse")

inventory_b.add_product(mouse)                                        # 4. add SAME object to B
check("The same Product object is now in Inventory B", inventory_b.find_product("P002") is mouse)
check("remove_product() returns False for a missing product",
      inventory_a.remove_product("NOPE") is False)
check("find_product() returns None for a missing product", inventory_b.find_product("NOPE") is None)

# ------------------------------------------------------------------
print("\n=== Section 4: Composition (Order and OrderLine) ===")
order_1 = Order("O001")
order_1.add_order_line(laptop, 2)       # the Order creates the OrderLine itself
order_1.add_order_line(antivirus, 3)
order_1.display_order()
check("Order 1 created 2 OrderLines", len(order_1.get_order_lines()) == 2)
check("calculate_subtotal() = price x quantity",
      order_1.get_order_lines()[0].calculate_subtotal() == 2400.0)
check("calculate_total() adds the subtotals", order_1.calculate_total() == 2549.7)

print("\nPredict first: same Product in two different Orders")
order_2 = Order("O002")
order_2.add_order_line(laptop, 1)
line_in_order_1 = order_1.get_order_lines()[0]
line_in_order_2 = order_2.get_order_lines()[0]
print("Same OrderLine object? ", line_in_order_1 is line_in_order_2)
print("Same Product object?   ", line_in_order_1.get_product() is line_in_order_2.get_product())
print("id(line 1) == id(line 2)?", id(line_in_order_1) == id(line_in_order_2))
check("Each Order created its OWN OrderLine", line_in_order_1 is not line_in_order_2)
check("Both OrderLines refer to the ONE laptop Product",
      line_in_order_1.get_product() is laptop and line_in_order_2.get_product() is laptop)

order_1.remove_order_line("D001")       # removed THROUGH the Order
order_1.display_order()
check("remove_order_line() removes the line through the Order",
      len(order_1.get_order_lines()) == 1)
check("Removing an OrderLine does NOT destroy the Product", antivirus.get_name() == "Antivirus Software")

check("get_order_lines() is read-only (a tuple, no append)",
      not hasattr(order_1.get_order_lines(), "append"))

try:
    order_1.add_order_line(laptop, 0)
    check("Quantity 0 is rejected", False)
except ValueError as error:
    print("Quantity 0 rejected:", error)
    check("Quantity 0 is rejected", True)

# ------------------------------------------------------------------
print("\n=== Section 6: LSP (substitutability) ===")
show_product_details(laptop)       # the SAME function...
show_product_details(antivirus)    # ...works for both subclasses

for product in [laptop, antivirus]:
    old_stock = product.get_stock()
    check(f"{product.get_name()}: update_stock(5) returns True and sets 5",
          product.update_stock(5) is True and product.get_stock() == 5)
    check(f"{product.get_name()}: update_stock(-1) returns False, stock unchanged",
          product.update_stock(-1) is False and product.get_stock() == 5)
    product.update_stock(old_stock)
    check(f"{product.get_name()}: get_fulfilment_info() returns a str",
          isinstance(product.get_fulfilment_info(), str))

# ------------------------------------------------------------------
print("\n=== Section 7: Polymorphism (one loop, no isinstance) ===")
shop = Inventory()
shop.add_product(laptop)
shop.add_product(antivirus)
messages = []
for product in shop.get_products():
    product.display_information()
    message = product.get_fulfilment_info()
    print(message)
    messages.append(message)
check("Physical product gave its own fulfilment message",
      messages[0] == "Requires physical shipping.")
check("Digital product gave its own fulfilment message",
      messages[1] == "Delivered digitally via a download link.")

# ------------------------------------------------------------------
print("\n=== Integration: save and load keep the Supplier link ===")
temp_file = os.path.join(tempfile.gettempdir(), "lab8_test_inventory.json")
save_inventory(shop, temp_file)
loaded = load_inventory(temp_file)
loaded_laptop = loaded.find_product("P001")
loaded_antivirus = loaded.find_product("D001")
assert loaded_laptop is not None and loaded_antivirus is not None   # find_product may return None
check("Loaded products are the correct subclasses",
      type(loaded_laptop) is PhysicalProduct and type(loaded_antivirus) is DigitalProduct)
check("Loaded product still has its Supplier",
      loaded_laptop.get_supplier().get_supplier_id() == "S001")
check("Products from the same supplier share ONE Supplier object after loading",
      loaded_laptop.get_supplier() is loaded_antivirus.get_supplier())
os.remove(temp_file)

# ------------------------------------------------------------------
print(f"\n{passed} passed, {failed} failed")