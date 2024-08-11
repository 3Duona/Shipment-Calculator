"""Import modules and functions for unit testing.

- sys: For capturing and restoring standard output.
- unittest: For defining and running test cases.
- StringIO: For capturing output streams during tests.
- vinted: Functions to be tested.
"""

import sys
import unittest
from io import StringIO

from vinted import process_transactions, validate_transactions, write_output


class TestShippingCalculator(unittest.TestCase):
    """Unit tests for the shipping calculator functions."""

    def test_validate_transactions_valid(self):
        """Test validating a list of valid transactions."""
        raw_transactions = ["2024-08-09 S LP", "2024-08-10 M MR"]
        expected_result = [
            ("2024-08-09", "S", "LP"),
            ("2024-08-10", "M", "MR"),
        ]
        result = validate_transactions(raw_transactions)
        self.assertEqual(result, expected_result)

    def test_validate_transactions_invalid_format(self):
        """Test validating transactions with invalid formats."""
        raw_transactions = ["2024-08-09 S", "Invalid Transaction"]
        expected_result = [
            ("2024-08-09 S", "Ignored"),
            ("Invalid Transaction", "Ignored"),
        ]
        result = validate_transactions(raw_transactions)
        self.assertEqual(result, expected_result)

    def test_validate_transactions_invalid_date(self):
        """Test validating transactions with invalid dates."""
        raw_transactions = ["2024-13-01 S LP", "2024-02-30 M MR"]
        expected_result = [
            ("2024-13-01 S LP", "Ignored"),
            ("2024-02-30 M MR", "Ignored"),
        ]
        result = validate_transactions(raw_transactions)
        self.assertEqual(result, expected_result)

    def test_validate_transactions_invalid_provider(self):
        """Test validating transactions with invalid providers."""
        raw_transactions = ["2024-08-09 S XY", "2024-08-10 L AB"]
        expected_result = [
            ("2024-08-09 S XY", "Ignored"),
            ("2024-08-10 L AB", "Ignored"),
        ]
        result = validate_transactions(raw_transactions)
        self.assertEqual(result, expected_result)

    def test_process_transactions(self):
        """Test processing a list of validated transactions."""
        transactions = [
            ("2024-08-09", "S", "LP"),
            ("2024-08-10", "L", "LP"),
            ("2024-08-11", "L", "LP"),
            ("2024-08-12", "L", "LP"),
        ]
        expected_output = [
            "2024-08-09 S LP 1.50 -",
            "2024-08-10 L LP 6.90 -",
            "2024-08-11 L LP 6.90 -",
            "2024-08-12 L LP 0.00 6.90",
        ]
        result = process_transactions(transactions)
        self.assertEqual(result, expected_output)

    def test_write_output(self):
        """Test capturing output from the write_output function."""
        output = ["2024-08-09 S LP 1.50 -", "2024-08-10 M MR 3.00 -"]
        captured_output = StringIO()
        sys.stdout = captured_output
        write_output(output)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "\n".join(output))


if __name__ == "__main__":
    unittest.main()
