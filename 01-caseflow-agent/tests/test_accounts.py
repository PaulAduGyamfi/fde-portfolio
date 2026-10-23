import pytest
from caseflow.accounts import normalize_account_id


@pytest.mark.parametrize("raw,expected", [
    ("ACC-18422", "ACC-18422"),   # already canonical
    ("77385",     "ACC-77385"),   # bare digits, from case_003
    ("AC8831",    "ACC-8831"),    # missing a C and the dash, from case_004
    ("acc 1001",  "ACC-1001"),    # lowercase with a space
    ("ACC--220",  "ACC-220"),     # doubled separator
    (None,        None),
    ("",          None),
    ("no digits", None),
])
def test_normalizes(raw, expected):
    assert normalize_account_id(raw) == expected