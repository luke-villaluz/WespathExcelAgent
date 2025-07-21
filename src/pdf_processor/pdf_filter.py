import re
from typing import Any, Dict, List, Optional


def extract_cash_transactions(text: str) -> Dict[str, Dict[str, List[float]]]:
    """Extract all cash deposits and withdrawals from PDF text, organized by series."""

    result = {
        "P": {"W": [], "D": []},  # Series P: Withdrawals and Deposits
        "I": {"W": [], "D": []},  # Series I: Withdrawals and Deposits
    }

    # Split text into lines for easier processing
    lines = text.split("\n")

    # Determine which page we're on by looking for account names
    current_series = None

    for i, line in enumerate(lines):
        # Check for account names to determine series
        if "WESPATH FUNDS TRUST XOPONANCE SVCE" in line:
            current_series = "P"
        elif "WESPATH XPONANCE SVCEF I" in line:
            current_series = "I"

        # Look for cash deposit transactions
        if "CASH DEPOSIT" in line and current_series:
            # Look for amount in the same line or nearby lines
            amount = extract_amount_from_line(line)
            if amount:
                result[current_series]["D"].append(amount)
            else:
                # Check nearby lines for amount
                for j in range(max(0, i - 2), min(len(lines), i + 3)):
                    if j != i:
                        amount = extract_amount_from_line(lines[j])
                        if amount:
                            result[current_series]["D"].append(amount)
                            break

        # Look for cash withdrawal transactions
        elif "CASH WITHDRAW" in line and current_series:
            # Look for amount in the same line or nearby lines
            amount = extract_amount_from_line(line)
            if amount:
                result[current_series]["W"].append(amount)
            else:
                # Check nearby lines for amount
                for j in range(max(0, i - 2), min(len(lines), i + 3)):
                    if j != i:
                        amount = extract_amount_from_line(lines[j])
                        if amount:
                            result[current_series]["W"].append(amount)
                            break

    return result


def extract_amount_from_line(line: str) -> Optional[float]:
    """Extract dollar amount from a line of text."""
    try:
        # Pattern for dollar amounts: $1,234.56 or 1,234.56 (including negative)
        # Look for amounts with commas and decimals
        amount_pattern = r"[\$]?(-?[\d,]+\.\d{2})"
        matches = re.findall(amount_pattern, line)

        if matches:
            # Take the first match and convert to float
            amount_str = matches[0].replace(",", "")
            amount_float = float(amount_str)

            # Only return if it's a reasonable amount (not 1.0 which is probably from exchange rate)
            if (
                abs(amount_float) > 10
            ):  # Filter out small amounts that are likely not transaction amounts
                return amount_float

        return None
    except Exception as e:
        print(f"Error extracting amount from line: {e}")
        return None
