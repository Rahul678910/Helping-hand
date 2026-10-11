"""Write your Python code in this file!

CodingBase Verify will inspect your functions, execute sandboxed tests,
and compute your Code Confidence Score (0-100%).

To verify this file, run:
    python verify.py your_file.py
"""


def clean_customer_data(records: list) -> list:
    """Clean and filter invalid customer rows from a dataset.

    Args:
        records: A list of customer record dictionaries.

    Returns:
        A list of validated records that contain an 'id'.
    """
    if not records:
        return []

    cleaned = []
    for row in records:
        if isinstance(row, dict) and row.get("id"):
            cleaned.append(row)
    return cleaned


def calculate_discount(price: float, rate: float = 0.1) -> float:
    """Calculate the final discounted price.

    Args:
        price: Base item price (must be non-negative).
        rate: Discount rate percentage between 0.0 and 1.0 (default 10%).

    Returns:
        The rounded price after discount.
    """
    if price < 0 or rate < 0:
        raise ValueError("Price and discount rate must be non-negative")
    return round(price * (1 - rate), 2)


def validate_email_address(email: str) -> bool:
    """Check if a string looks like a valid basic email address.

    Args:
        email: The email address string to validate.

    Returns:
        True if the email has valid format with '@' and '.', False otherwise.
    """
    if not email or not isinstance(email, str):
        return False
    email = email.strip()
    return "@" in email and "." in email.split("@")[-1]
