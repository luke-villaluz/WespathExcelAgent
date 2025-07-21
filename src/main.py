# src/main.py
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Your existing modules
from excel_processor.excel_extractor import extract_all_data
from excel_processor.excel_filter import extract_cash_transactions_by_series
from excel_processor.excel_updater import update_excel_with_transactions


def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)

    # Configure logging with UTF-8 encoding
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/wespath_agent.log", mode="w", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )
    return logging.getLogger(__name__)


def main():
    """Main Wespath Excel Agent workflow"""
    logger = setup_logging()
    logger.info("Starting Wespath Excel Agent")

    try:
        # Load environment variables
        load_dotenv()

        # Get file paths from environment (with defaults for local testing)
        cash_statement_path = Path(
            os.getenv(
                "CASH_STATEMENT_PATH",
                "Wespath Spreadsheet Files/Wespath Bank Projected Cash Statement_16 Jul 2025.xlsx",
            )
        )
        tracking_template_path = Path(
            os.getenv(
                "TRACKING_TEMPLATE_PATH",
                "Wespath Spreadsheet Files/Wespath Account Tracking_Template_Latest 071625.xlsx",
            )
        )

        # Validate files exist
        if not cash_statement_path.exists():
            raise FileNotFoundError(f"Cash statement not found: {cash_statement_path}")
        if not tracking_template_path.exists():
            raise FileNotFoundError(
                f"Tracking template not found: {tracking_template_path}"
            )

        logger.info(f"Processing cash statement: {cash_statement_path}")

        # 1. Extract data from cash statement
        cash_data = extract_all_data(cash_statement_path)
        logger.info(
            f"Extracted {len(cash_data['data'])} rows from {cash_data['worksheet_name']}"
        )

        # 2. Filter transactions by series
        transactions = extract_cash_transactions_by_series(cash_data)
        logger.info(
            f"Filtered transactions: P={len(transactions['P']['W'])}W/{len(transactions['P']['D'])}D, I={len(transactions['I']['W'])}W/{len(transactions['I']['D'])}D"
        )

        # 3. Update tracking template
        logger.info(f"Updating tracking template: {tracking_template_path}")
        success = update_excel_with_transactions(tracking_template_path, transactions)

        if success:
            logger.info("Wespath Excel Agent completed successfully!")
            return True
        else:
            logger.error("Failed to update tracking template")
            return False

    except Exception as e:
        logger.error(f"Wespath Excel Agent failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
