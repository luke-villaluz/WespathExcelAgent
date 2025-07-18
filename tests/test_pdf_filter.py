import pytest
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

sys.path.append('src')

from pdf_processor.pdf_extractor import extract_all_text
from pdf_processor.pdf_filter import extract_cash_transactions

# Load environment variables
load_dotenv()

def test_pdf_filter_cash_deposits():
    """Test the actual PDF filter logic with extracted text."""
    # Get PDF path from environment variable
    test_pdf_path = os.getenv('TEST_PDF_PATH')
    
    if not test_pdf_path:
        pytest.skip("TEST_PDF_PATH not set in .env file")
    
    pdf_path = Path(test_pdf_path)
    
    if not pdf_path.exists():
        pytest.skip(f"Test PDF file not found: {pdf_path}")
    
    print(f"Testing PDF filter logic with: {pdf_path}")
    
    # Extract all text from PDF
    text = extract_all_text(pdf_path)
    
    print(f"Extracted {len(text)} characters")
    
    # Test the filter
    transactions = extract_cash_transactions(text)
    
    print(f"Found transactions:")
    print(f"  Series P - WITHDRAW: {transactions['P']['W']}")
    print(f"  Series P - DEPOSIT: {transactions['P']['D']}")
    print(f"  Series I - WITHDRAW: {transactions['I']['W']}")
    print(f"  Series I - DEPOSIT: {transactions['I']['D']}")
    
    # Assertions
    assert len(transactions['P']['W']) >= 1, "Should find at least 1 cash withdrawal in Series P"
    assert len(transactions['I']['D']) >= 1, "Should find at least 1 cash deposit in Series I"
    
    # Check specific amounts
    assert -53977.40 in transactions['P']['W'], f"Should find withdrawal amount -53977.40 in Series P, found {transactions['P']['W']}"
    assert 914072.50 in transactions['I']['D'], f"Should find deposit amount 914072.50 in Series I, found {transactions['I']['D']}"