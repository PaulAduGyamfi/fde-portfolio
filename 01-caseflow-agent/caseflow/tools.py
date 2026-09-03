from agents import function_tool

ACCOUNTS = {
    "ACC-1001": {"name": "Jordan Lee", "plan": "Pro", "status": "active", "region": "US"}, 
    "ACC-2002": {"name": "Sam Ortiz", "plan": "Basic", "status": "locked", "region": "EU"}
    }
CASES = {
    "ACC-1001": [{"case_id": "K-9", "status": "open", "topic": "refund", "opened": "2026-08-20"}], 
    "ACC-2002": [{"case_id": "K-12", "status": "open", "topic": "login", "opened": "2026-08-28"}]
    }

ALLOWED = set(ACCOUNTS)

def _get_account(account_id: str) -> dict:
    """
    Return a sanitized account summary (name, plan, status, region) for an allowed account ID.
    """ 
    if account_id not in ALLOWED:
        return {"error": "account_not_found_or_not_permitted"} 
    return ACCOUNTS[account_id]

@function_tool
def get_account(account_id: str) -> dict:
    """
    Return a sanitized account summary (name, plan, status, region) for an allowed account ID.
    """
    return _get_account(account_id)


def _list_open_cases(account_id: str) -> list[dict]:
    """
    Return open support cases (case_id, status, topic, opened) for an allowed account ID.
    """ 
    return CASES.get(account_id, []) if account_id in ALLOWED else []

@function_tool
def list_open_cases(account_id: str) -> list[dict]:
    """
    Return open support cases (case_id, status, topic, opened) for an allowed account ID.
    """ 
    return _list_open_cases(account_id)

def _create_draft_reply(account_id: str, summary: str, proposed_text: str) -> dict:
    """
    Store a DRAFT reply for human review. Does not send anything. Returns the draft id.
    """
    draft_id = f"D-{abs(hash(proposed_text)) % 10000}"
    DRAFTS[draft_id] = {"account_id": account_id, "summary": summary, "text": proposed_text, "status": "pending_review"} 
    return {"draft_id": draft_id, "status": "pending_review"}

@function_tool
def create_draft_reply(account_id: str, summary: str, proposed_text: str) -> dict:
    """
    Store a DRAFT reply for human review. Does not send anything. Returns the draft id.
    """
    return _create_draft_reply(account_id, summary, proposed_text)
    
DRAFTS: dict[str, dict] = {}