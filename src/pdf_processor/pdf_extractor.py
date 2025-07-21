from pathlib import Path

import pdfplumber


def extract_all_text(pdf_path: Path) -> str:
    """Extract ALL text from a PDF file."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n"
            return all_text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""
