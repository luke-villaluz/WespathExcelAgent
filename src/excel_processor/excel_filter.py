from typing import Any, Dict, List


def extract_cash_transactions_by_series(
    data: Dict[str, Any]
) -> Dict[str, Dict[str, List[float]]]:
    """Extract cash transactions organized by series (P and I) from Excel data."""

    result = {
        "P": {"W": [], "D": []},  # Series P: Withdrawals and Deposits
        "I": {"W": [], "D": []},  # Series I: Withdrawals and Deposits
    }

    # Get the data rows (skip header row)
    rows = data["data"][1:]  # Skip row 0 (headers)

    for i, row in enumerate(rows):
        if len(row) < 50:  # Skip rows that don't have enough columns
            continue

        # Extract key information from the row
        cash_account_name = (
            row[3] if len(row) > 3 else ""
        )  # Column D: Cash Account Name
        transaction_type = (
            row[20] if len(row) > 20 else ""
        )  # Column U: Transaction Type
        transaction_amount = (
            row[47] if len(row) > 47 else None
        )  # Column AS: Transaction Amount Local

        # Debug output
        print(
            f"Row {i+1}: Account='{cash_account_name}', Type='{transaction_type}', Amount={transaction_amount}"
        )

        # Determine series based on account name (normalize spaces)
        series = None
        normalized_account = " ".join(
            str(cash_account_name).split()
        )  # Remove extra spaces

        if "WESPATH FUNDS TRUST XOPONANCE SVCE" in normalized_account:
            series = "P"
        elif "WESPATH XPONANCE SVCEF I" in normalized_account:
            series = "I"

        # Process transaction if we have a valid series and amount
        if series and transaction_amount is not None and transaction_amount != "":
            try:
                amount = float(transaction_amount)

                # Determine if it's a withdrawal or deposit based on transaction type
                if transaction_type == "CASH WITHDRAW":
                    result[series]["W"].append(amount)
                    print(f"  -> Added withdrawal {amount} to Series {series}")
                elif transaction_type == "CASH DEPOSIT":
                    result[series]["D"].append(amount)
                    print(f"  -> Added deposit {amount} to Series {series}")

            except (ValueError, TypeError):
                # Skip if amount can't be converted to float
                continue

    return result
