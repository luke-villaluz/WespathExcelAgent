import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

sys.path.append("src")

from pdf_processor.pdf_extractor import extract_all_text

# Load environment variables
load_dotenv()


def test_extractor_finds_pdf_files():
    """Test that we can find PDF files in the directory."""
    pdf_dir = Path("Wespath Spreadsheet Files")
    pdf_files = list(pdf_dir.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files in directory")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")

    assert (
        len(pdf_files) > 0
    ), "No PDF files found in Wespath Spreadsheet Files directory"


def test_extractor_extracts_text():
    """Test that the extractor can extract text from a specific PDF."""
    # Get PDF path from environment variable
    test_pdf_path = os.getenv("TEST_PDF_PATH")

    if not test_pdf_path:
        pytest.skip("TEST_PDF_PATH not set in .env file")

    pdf_path = Path(test_pdf_path)

    if not pdf_path.exists():
        pytest.skip(f"Test PDF file not found: {pdf_path}")

    print(f"Testing extractor with: {pdf_path}")

    # Extract all text
    text = extract_all_text(pdf_path)

    print(f"Extracted {len(text)} characters")
    print("Complete extracted text:")
    print("-" * 80)
    print(text)
    print("-" * 80)

    # Basic assertions
    assert len(text) > 0, "Extracted text should not be empty"
    assert (
        "CASH DEPOSIT" in text or "CASH WITHDRAW" in text
    ), "Should contain cash transactions"
