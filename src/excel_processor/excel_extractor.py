import openpyxl
from pathlib import Path
from typing import Dict, Any

def extract_all_data(excel_path: Path) -> Dict[str, Any]:
    """Extract all data from Excel file."""
    try:
        workbook = openpyxl.load_workbook(excel_path)
        worksheet = workbook.active
        
        # Check if worksheet exists
        if worksheet is None:
            print(f"No active worksheet found in {excel_path}")
            return {'worksheet_name': '', 'data': []}
        
        # Get all data from the worksheet
        all_data = []
        for row in worksheet.iter_rows(values_only=True):
            all_data.append(row)
        
        return {
            'worksheet_name': worksheet.title,
            'data': all_data
        }
    except Exception as e:
        print(f"Error extracting data from {excel_path}: {e}")
        return {'worksheet_name': '', 'data': []}
