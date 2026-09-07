from .schemas import EmailIn, Extraction
from .extract import extract
from .tools import _get_account, _list_open_cases, _create_draft_reply, DRAFTS 
from agents import Agent, Runner

drafter = Agent(
    name="ServiceOps Drafter",
    instructions=("Write a concise, polite reply to the customer using ONLY the facts provided. "
    "If facts are missing, ask for them. Never promise refunds or account changes."),
    )

def policy_check(draft: str, facts: dict) -> list[str]:
    """
    Deterministic checks. Returns a list of violations (empty = pass).
    """
    v = []
    for banned in ["refund has been issued", "your account is now", "password is"]:
        if banned in draft.lower(): 
            v.append(f"banned phrase: {banned}")
    if facts.get("account", {}).get("status") == "locked" and "unlock" in draft.lower():
        v.append("promises unlock on locked account") 
    return v

async def handle(email: EmailIn) -> dict:
    ex: Extraction = await extract(email)
    if ex.needs_human_review:
        return {"status": "escalated", "reason": "needs_human_review", "extraction": ex.model_dump()}
    if ex.account_id is None:
        return {"status": "needs_information", "missing": ex.missing_information}
    facts = {"account": _get_account(ex.account_id), "cases": _list_open_cases(ex.account_id)}
    prompt = f"Customer intent: {ex.intent}. Request: {ex.requested_action}\nFacts: {facts}"
    draft = (await Runner.run(drafter, prompt, max_turns=1)).final_output
    violations = policy_check(draft, facts)
    if violations:
        return {"status": "blocked_by_policy", "violations": violations, "draft": draft}
    d = _create_draft_reply(ex.account_id, ex.requested_action, draft)
    return {"status": "awaiting_approval", "draft_id": d["draft_id"], "draft": draft}