total_inventory = 0
rejected_entries = 0

while True:
    entry = input("Enter stock quantity or 'quit' to exit: ").strip()

    if entry.lower() == "quit":
        break

    try:
        quantity = int(float(entry))
    except ValueError:
        print("Invalid input. Please enter a valid stock quantity or 'quit' to exit.")
        rejected_entries += 1
        continue

    if quantity < 0:
        print("Invalid input. Please enter a non-negative stock quantity.")
        rejected_entries += 1
        continue

    if total_inventory + quantity > 500:
        print(f"Overstock alert! You cannot add {quantity} items. Maximum capacity is 500.")
        rejected_entries += 1
        break

    total_inventory += quantity
    print(f"Added {quantity} items to inventory. Total inventory: {total_inventory}")

print(f"Total Units Processed: {total_inventory}")
print(f"Total rejected entries: {rejected_entries}")
