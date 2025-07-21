import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

sys.path.append("src")

from excel_processor.excel_extractor import extract_all_data
from excel_processor.excel_filter import extract_cash_transactions_by_series

# Load environment variables
load_dotenv()


def test_excel_filter_cash_transactions():
    """Test the actual Excel filter logic with extracted data."""
    # Get Excel path from environment variable
    test_excel_path = os.getenv("TEST_EXCEL_PATH")

    if not test_excel_path:
        pytest.skip("TEST_EXCEL_PATH not set in .env file")

    excel_path = Path(test_excel_path)

    if not excel_path.exists():
        pytest.skip(f"Test Excel file not found: {excel_path}")

    print(f"Testing Excel filter logic with: {excel_path}")

    # Extract all data from Excel
    data = extract_all_data(excel_path)

    print(f"Extracted data from worksheet: {data['worksheet_name']}")
    print(f"Number of rows: {len(data['data'])}")

    # Test the filter
    transactions = extract_cash_transactions_by_series(data)

    print(f"Found transactions:")
    print(f"  Series P - WITHDRAW: {transactions['P']['W']}")
    print(f"  Series P - DEPOSIT: {transactions['P']['D']}")
    print(f"  Series I - WITHDRAW: {transactions['I']['W']}")
    print(f"  Series I - DEPOSIT: {transactions['I']['D']}")

    # Assertions
    assert (
        len(transactions["P"]["W"]) >= 1
    ), "Should find at least 1 cash withdrawal in Series P"
    assert (
        len(transactions["I"]["D"]) >= 1
    ), "Should find at least 1 cash deposit in Series I"

    # Check specific amounts
    assert (
        -53977.4 in transactions["P"]["W"]
    ), f"Should find withdrawal amount -53977.4 in Series P, found {transactions['P']['W']}"
    assert (
        914072.5 in transactions["I"]["D"]
    ), f"Should find deposit amount 914072.5 in Series I, found {transactions['I']['D']}"
