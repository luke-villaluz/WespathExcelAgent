import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

sys.path.append("src")

from excel_processor.excel_extractor import extract_all_data

# Load environment variables
load_dotenv()


def test_excel_extractor_finds_excel_files():
    """Test that we can find Excel files in the directory."""
    excel_dir = Path("Wespath Spreadsheet Files")
    excel_files = list(excel_dir.glob("*.xlsx"))

    print(f"Found {len(excel_files)} Excel files in directory")
    for excel in excel_files:
        print(f"  - {excel.name}")

    assert (
        len(excel_files) > 0
    ), "No Excel files found in Wespath Spreadsheet Files directory"


def test_excel_extractor_extracts_data():
    """Test that the extractor can extract data from a specific Excel file."""
    # Get Excel path from environment variable
    test_excel_path = os.getenv("TEST_EXCEL_PATH")

    if not test_excel_path:
        pytest.skip("TEST_EXCEL_PATH not set in .env file")

    excel_path = Path(test_excel_path)

    if not excel_path.exists():
        pytest.skip(f"Test Excel file not found: {excel_path}")

    print(f"Testing Excel extractor with: {excel_path}")

    # Extract all data
    data = extract_all_data(excel_path)

    print(f"Extracted data from worksheet: {data['worksheet_name']}")
    print(f"Number of rows: {len(data['data'])}")

    # Show first few rows
    print("First 5 rows of data:")
    print("-" * 80)
    for i, row in enumerate(data["data"][:5]):
        print(f"Row {i+1}: {row}")
    print("-" * 80)

    # Basic assertions
    assert len(data["data"]) > 0, "Extracted data should not be empty"
    assert data["worksheet_name"] != "", "Worksheet name should not be empty"
    assert (
        len(data["data"]) >= 7
    ), "Should have at least 7 rows of data (header + 6 data rows)"
