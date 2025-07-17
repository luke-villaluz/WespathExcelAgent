import pytest
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

sys.path.append('src')

from pdf_processor.extractor import extract_all_text
from pdf_processor.filter import extract_cash_transactions

# Load environment variables
load_dotenv()

def test_filter_cash_deposits():
    """Test the actual filter logic with extracted text."""
    # Get PDF path from environment variable
    test_pdf_path = os.getenv('TEST_PDF_PATH')
    
    if not test_pdf_path:
        pytest.skip("TEST_PDF_PATH not set in .env file")
    
    pdf_path = Path(test_pdf_path)
    
    if not pdf_path.exists():
        pytest.skip(f"Test PDF file not found: {pdf_path}")
    
    print(f"Testing filter logic with: {pdf_path}")
    
    # Extract all text from PDF
    text = extract_all_text(pdf_path)
    
    print(f"Extracted {len(text)} characters")
    
    # Test the filter
    transactions = extract_cash_transactions(text)
    
    print(f"Found transactions:")
    print(f"  DEPOSIT: {transactions['DEPOSIT']}")
    print(f"  WITHDRAW: {transactions['WITHDRAW']}")
    
    # Assertions
    assert len(transactions['DEPOSIT']) >= 1, "Should find at least 1 cash deposit"
    assert len(transactions['WITHDRAW']) >= 1, "Should find at least 1 cash withdrawal"
    
    # Check specific amounts
    assert 914072.50 in transactions['DEPOSIT'], f"Should find deposit amount 914072.50, found {transactions['DEPOSIT']}"
    assert -53977.40 in transactions['WITHDRAW'], f"Should find withdrawal amount -53977.40, found {transactions['WITHDRAW']}"