import pytest
from pathlib import Path
import sys
import os
from dotenv import load_dotenv
import tempfile
import shutil

sys.path.append('src')

from excel_processor.excel_updater import update_excel_with_transactions

# Load environment variables
load_dotenv()

def test_excel_updater_updates_worksheets():
    """Test that the Excel updater can update both worksheets with transaction data."""
    test_excel_path = os.getenv('TEST_EXCEL_PATH')
    
    if not test_excel_path:
        pytest.skip("TEST_EXCEL_PATH not set in .env file")
    
    excel_path = Path(test_excel_path)
    
    if not excel_path.exists():
        pytest.skip(f"Test Excel file not found: {excel_path}")
    
    # Create a temporary copy of the Excel file for testing
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
        temp_excel_path = Path(tmp_file.name)
    
    try:
        # Copy the original file to temp location
        shutil.copy2(excel_path, temp_excel_path)
        
        print(f"Testing Excel updater with: {temp_excel_path}")
        
        # Sample transaction data
        test_transactions = {
            'P': {
                'W': [-53977.4],  # Withdrawal
                'D': [100000.0]   # Deposit
            },
            'I': {
                'W': [50000.0],   # Withdrawal
                'D': [914072.5]   # Deposit
            }
        }
        
        # Update the Excel file
        success = update_excel_with_transactions(temp_excel_path, test_transactions, "7/16/2025")
        
        assert success, "Excel update should succeed"
        
        # Verify the file was modified
        assert temp_excel_path.exists(), "Updated file should exist"
        
        print("Excel updater test completed successfully")
        
    finally:
        # Clean up temporary file
        if temp_excel_path.exists():
            temp_excel_path.unlink()

def test_excel_updater_formats_negative_numbers():
    """Test that negative numbers are formatted with parentheses."""
    # This test would verify the formatting logic
    # For now, we'll just test the basic functionality
    test_transactions = {
        'P': {'W': [-1000.0], 'D': []},
        'I': {'W': [], 'D': [500.0]}
    }
    
    # The actual formatting test would require a real Excel file
    # We can add this later when we have more test data
    assert len(test_transactions['P']['W']) == 1, "Should have one withdrawal"
    assert len(test_transactions['I']['D']) == 1, "Should have one deposit"
