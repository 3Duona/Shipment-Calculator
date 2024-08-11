"""Import necessary modules.

- datetime: For date validation and manipulation.
- defaultdict: For efficient tracking of discounts and transaction counts.
"""

import datetime
from collections import defaultdict

# Constants of vendors and shipment pricings
PRICES = {
    "LP": {"S": 1.50, "M": 4.90, "L": 6.90},
    "MR": {"S": 2.00, "M": 3.00, "L": 4.00},
}


def read_transactions(file_name="input.txt"):
    """Read transactions from a file and return a list of transaction strings.

    Args:
    ----
        file_name (str): The name of the file containing transactions.

    Returns:
    -------
        list: A list of raw transaction strings.

    """
    with open(file_name, encoding="utf-8") as file:
        transactions = file.readlines()

    # Remove leading and trailing whitespace from each transaction string
    return [transaction.strip() for transaction in transactions]


def validate_transactions(raw_transactions):
    """Validate a list of transaction strings and return a list of valid transactions.

    Args:
    ----
        raw_transactions (list): A list of raw transaction strings.

    Returns:
    -------
        list: A list of validated transactions where each transaction is either a tuple
              (date, size, provider) or (transaction, 'Ignored') if the transaction is invalid.

    """
    # A list to store validated transactions
    validated_transactions = []

    for transaction in raw_transactions:
        validated_transaction = check_transaction(transaction)
        validated_transactions.append(validated_transaction)

    return validated_transactions


def check_transaction(transaction):
    """Validate the format of a single transaction and return it as a tuple.

    Args:
    ----
        transaction (str): A string representing a single transaction.

    Returns:
    -------
        tuple: If the transaction is valid, returns a tuple (date, size, provider).
               If invalid, returns a tuple (transaction, 'Ignored').

    """
    # Valid package sizes and courier providers
    valid_sizes = {"S", "M", "L"}
    valid_providers = {"LP", "MR"}

    parts = transaction.split()

    if len(parts) != 3:
        return (transaction, "Ignored")

    date, size, provider = parts

    # Check if the date is in ISO format (YYYY-MM-DD)
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return (transaction, "Ignored")

    # Check if size and provider are valid
    if size not in valid_sizes or provider not in valid_providers:
        return (transaction, "Ignored")

    return (date, size, provider)


def process_transactions(transactions):
    """Process a list of transactions to apply discounts and return a list of formatted transactions.

    Args:
    ----
        transactions (list): A list of tuples representing transactions.
        Each tuple contains (date, size, provider) or (transaction, 'Ignored').

    Returns:
    -------
        list: A list of formatted strings representing the processed
        transactions with applicable discounts and adjustments.

    """
    # A list to store proccessed transactions
    processed_transactions = []

    # Initialize the dictionary for tracking discounts
    tracking_data = defaultdict(lambda: {"L_LP_count": 0, "discount": 0.0})

    for entry in transactions:
        # Skip all entries with 'Ignored' as the last element of the tuple
        if (
            isinstance(entry, tuple)
            and len(entry) > 0
            and entry[-1] == "Ignored"
        ):
            cleaned_transaction = " ".join(part.strip() for part in entry)
            processed_transactions.append(cleaned_transaction)
            continue

        if isinstance(entry, tuple) and len(entry) == 3:
            date, size, provider = entry

            # Extract year-month from date
            year_month = date[:7]

            # Get the price for the current provider and size
            price = PRICES[provider].get(size, 0.0)

            # Calculate discount based on size and provider
            new_price, discount_amount = calculate_discount(
                size,
                provider,
                year_month,
                tracking_data,
            )

            # Format the processed transactions based on the results
            if new_price == price and discount_amount == 0.0:
                processed_transactions.append(
                    f"{date} {size} {provider} {price:.2f} -",
                )
            else:
                processed_transactions.append(
                    f"{date} {size} {provider} {new_price:.2f} {discount_amount:.2f}",
                )

    return processed_transactions


def calculate_discount(size, provider, year_month, tracking_data):
    """Calculate the discount based on size and provider.

    Args:
    ----
        size (str): The size of the shipment.
        provider (str): The provider of the shipment.
        year_month (str): The year and month of the transaction.
        tracking_data (dict): A dictionary tracking discounts and counts for each month.

    Returns:
    -------
        tuple: A tuple containing the new price and discount amount.

    """
    # Monthly limit for discounts
    monthly_limit = 10.0

    if size == "L" and provider == "LP":
        tracking_data[year_month]["L_LP_count"] += 1
        current_count = tracking_data[year_month]["L_LP_count"]

        # Check if it's third L shipment of the month
        if current_count == 3:
            discount_amount = PRICES[provider]["L"]
            total_discount = (
                tracking_data[year_month]["discount"] + discount_amount
            )

            if total_discount > monthly_limit:
                discount_amount = (
                    monthly_limit - tracking_data[year_month]["discount"]
                )
                tracking_data[year_month]["discount"] += discount_amount
                new_price = PRICES[provider]["L"] - discount_amount
                return new_price, discount_amount
            else:
                tracking_data[year_month]["discount"] += discount_amount
                return 0.0, discount_amount
        else:
            return PRICES[provider]["L"], 0.0

    elif size == "S":
        # Calculate the lowest price for small size shipments
        lowest_price_size_s = min(PRICES["LP"]["S"], PRICES["MR"]["S"])
        discount_amount = PRICES[provider]["S"] - lowest_price_size_s

        if discount_amount != 0:
            if (
                tracking_data[year_month]["discount"] + discount_amount
                > monthly_limit
            ):
                discount_amount = (
                    monthly_limit - tracking_data[year_month]["discount"]
                )
                tracking_data[year_month]["discount"] += discount_amount
                new_price = PRICES[provider]["S"] - discount_amount
                return new_price, discount_amount
            else:
                tracking_data[year_month]["discount"] += discount_amount
                return lowest_price_size_s, discount_amount
        else:
            return PRICES[provider]["S"], 0.0

    # If no discount conditions are met, return the original price and zero discount
    return PRICES[provider].get(size, 0.0), 0.0


def write_output(output):
    """Write the processed output to the standard output (console).

    Args:
    ----
        output (list): A list of formatted strings of processed transactions.

    """
    for line in output:
        print(line)


def main():
    """Handle reading, validating, processing, and displaying transactions."""
    raw_transactions = read_transactions()
    validated_transactions = validate_transactions(raw_transactions)
    processed_transactions = process_transactions(validated_transactions)
    write_output(processed_transactions)


if __name__ == "__main__":
    main()
