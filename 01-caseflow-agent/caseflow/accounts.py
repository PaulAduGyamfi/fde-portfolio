import re

CANONICAL = re.compile(r"^ACC-\d+$")


def normalize_account_id(raw: str | None) -> str | None:
    """
    Canonicalize whatever the model returned into 'ACC-<digits>'.
    Returns None when there is nothing to normalize.
    """
    if raw is None:
        return None
    digits = re.sub(r"\D", "", raw)
    if not digits:
        return None
    return f"ACC-{digits}"