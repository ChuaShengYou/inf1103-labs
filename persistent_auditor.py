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

def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

            # If file is empty, start fresh
            if len(lines) == 0:
                return 0, []
            
            # Load total inventory
            total_inventory = int(lines[0])

            # Load transaction history
            history = []

            if len(lines) > 1:
                history_line = lines[1].strip()

                if history_line:
                    history_data = history_line.split(",")

                    for x in history_data:
                        history.append(int(x))

    except FileNotFoundError:
        total_inventory = 0
        history = []

    return total_inventory, history

def save_inventory(total_inventory, history):
    with open("inventory.txt", "w") as file:
        file.write(str(total_inventory) + "\n")

        history_txt = ",".join(str(x) for x in history)
        file.write(history_txt)

def main():
    """
    Main function to run inventory auditor program.
    """
    # local variables
    tax_amount = 0
    failed_entries = 0
    exit_program = False

    inventory, history = load_inventory()

    while not exit_program:
        result = get_valid_input()

        if result == "quit":
            save_inventory(inventory, history)
            exit_program = True
            continue

        if result is None:
            failed_entries += 1
            continue

        new_total = process_delivery(inventory, result)

        if new_total > MAX_CAPACITY:
            print(f"Overstock alert! You cannot add {result} items. Maximum capacity is {MAX_CAPACITY}.")
            failed_entries += 1
            save_inventory(inventory, history)
            exit_program = True
            continue

        inventory = new_total
        history.append(result)
        tax_amount += calculate_tax(result)
        print(f"Added {result} items to inventory. Total inventory: {inventory} (Tax for this delivery: {calculate_tax(result):.2f})")

    generate_report(inventory, failed_entries)
    print(f"Total Tax Collected: {tax_amount:.2f}")


# __name__ (Program Entry Point)
if __name__ == "__main__":
    main()
