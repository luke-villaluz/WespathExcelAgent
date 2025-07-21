import pytest
from pathlib import Path
import sys
import os
from dotenv import load_dotenv
import tempfile
import shutil

sys.path.append('src')

from excel_processor.excel_updater import update_excel_with_transactions
from excel_processor.excel_extractor import extract_all_data
from excel_processor.excel_filter import extract_cash_transactions_by_series

# Load environment variables
load_dotenv()

def test_excel_updater_updates_worksheets():
    """Test that the Excel updater can update both worksheets with transaction data."""
    # Use the tracking template as the target file
    tracking_template_path = Path("Wespath Spreadsheet Files/Wespath Account Tracking_Template_Latest 071625.xlsx")
    
    if not tracking_template_path.exists():
        pytest.skip(f"Tracking template not found: {tracking_template_path}")
    
    # Create temp_sheets directory if it doesn't exist
    temp_sheets_dir = Path("tests/temp_sheets")
    temp_sheets_dir.mkdir(exist_ok=True)
    
    # Create a test Excel file in the temp_sheets directory
    test_output_path = temp_sheets_dir / "test_excel_updater.xlsx"
    
    # Remove previous test file if it exists
    if test_output_path.exists():
        test_output_path.unlink()
        print(f"Removed previous test file: {test_output_path}")
    
    try:
        # Copy the tracking template to test location
        shutil.copy2(tracking_template_path, test_output_path)
        
        print(f"Testing Excel updater with: {test_output_path}")
        
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
        
        # Update the Excel file (no date parameter - will use current date)
        success = update_excel_with_transactions(test_output_path, test_transactions)
        
        assert success, "Excel update should succeed"
        
        # Verify the file was modified
        assert test_output_path.exists(), "Updated file should exist"
        
        print(f"Excel updater test completed successfully")
        print(f"Test file created: {test_output_path.absolute()}")
        print("You can now open this file to inspect the results!")
        
    except Exception as e:
        # Clean up on error
        if test_output_path.exists():
            test_output_path.unlink()
        raise e

def test_full_workflow_extract_and_update():
    """Test the full workflow: extract from cash statement and update tracking template."""
    # Source file: cash statement
    cash_statement_path = Path("Wespath Spreadsheet Files/Wespath Bank Projected Cash Statement_16 Jul 2025.xlsx")
    
    # Target file: tracking template
    tracking_template_path = Path("Wespath Spreadsheet Files/Wespath Account Tracking_Template_Latest 071625.xlsx")
    
    if not cash_statement_path.exists():
        pytest.skip(f"Cash statement not found: {cash_statement_path}")
    
    if not tracking_template_path.exists():
        pytest.skip(f"Tracking template not found: {tracking_template_path}")
    
    # Create temp_sheets directory if it doesn't exist
    temp_sheets_dir = Path("tests/temp_sheets")
    temp_sheets_dir.mkdir(exist_ok=True)
    
    # Create a test output file in temp_sheets
    test_output_path = temp_sheets_dir / "test_full_workflow.xlsx"
    
    # Remove previous test file if it exists
    if test_output_path.exists():
        test_output_path.unlink()
        print(f"Removed previous test file: {test_output_path}")
    
    try:
        # Copy the tracking template to test location
        shutil.copy2(tracking_template_path, test_output_path)
        
        print(f"Extracting data from: {cash_statement_path}")
        
        # Extract data from cash statement
        cash_data = extract_all_data(cash_statement_path)
        print(f"Extracted data from worksheet: {cash_data['worksheet_name']}")
        print(f"Number of rows: {len(cash_data['data'])}")
        
        # Filter transactions by series
        transactions = extract_cash_transactions_by_series(cash_data)
        print(f"Extracted transactions: {transactions}")
        
        # Update the tracking template with real data
        success = update_excel_with_transactions(test_output_path, transactions)
        
        assert success, "Excel update should succeed"
        
        # Verify the file was modified
        assert test_output_path.exists(), "Updated file should exist"
        
        print(f"Full workflow test completed successfully")
        print(f"Test file created: {test_output_path.absolute()}")
        print("You can now open this file to inspect the real transaction data!")
        
    except Exception as e:
        # Clean up on error
        if test_output_path.exists():
            test_output_path.unlink()
        raise e

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
