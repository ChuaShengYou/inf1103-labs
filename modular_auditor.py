# Global Constants
MAX_CAPACITY = 500
TAX_RATE = 0.1  # 10% tax rate


def get_valid_input():
    entry = input("Enter stock quantity or 'quit' to exit: ").strip()

    if entry.lower() == "quit":
        return "quit"

    try:
        quantity = int(float(entry))
    except ValueError:
        print("Invalid input. Please enter a valid stock quantity or 'quit' to exit.")
        return None

    if quantity < 0:
        print("Invalid input. Please enter a non-negative stock quantity.")
        return None

    return quantity


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * TAX_RATE
    return tax


def generate_report(total_units, failed_entries):
    print(f"Total Units Processed: {total_units}")
    print(f"Total rejected entries: {failed_entries}")


def main():
    """
    Main function to run inventory auditor program.
    """
    # local variables
    inventory = 0
    tax_amount = 0
    failed_entries = 0
    exit_program = False

    while not exit_program:
        result = get_valid_input()

        if result == "quit":
            exit_program = True
            continue

        if result is None:
            failed_entries += 1
            continue

        new_total = process_delivery(inventory, result)

        if new_total > MAX_CAPACITY:
            print(f"Overstock alert! You cannot add {result} items. Maximum capacity is {MAX_CAPACITY}.")
            failed_entries += 1
            exit_program = True
            continue

        inventory = new_total
        tax_amount += calculate_tax(result)
        print(f"Added {result} items to inventory. Total inventory: {inventory} (Tax for this delivery: {calculate_tax(result):.2f})")

    generate_report(inventory, failed_entries)
    print(f"Total Tax Collected: {tax_amount:.2f}")


# __name__ (Program Entry Point)
if __name__ == "__main__":
    main()
