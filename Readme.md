# Vinted Shipping Calculator

## Overview

1. **Read Data**: Load transactions from `input.txt`.

2. **Validation**:

   - Ensure data is formatted is correctly.
   - Validate the date is in ISO format (`YYYY-MM-DD`).
   - Check that package sizes and providers are valid.

3. **Processing**:
   - Ignore invalid transactions.
   - Apply discounts:
     - For large shipments from LP: The 3rd large shipment in a month is free.
     - For small shipments: Set the price to the lowest small package rate among providers.
     - Discounts for a single month cannot exceed 10 euro.

## Running Program

Execute `python vinted.py`

## Running Tests

Execute `python -m unittest unit_tests.py`
