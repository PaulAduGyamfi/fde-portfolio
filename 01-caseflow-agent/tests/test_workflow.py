import pytest
from caseflow.schemas import EmailIn, Extraction
from caseflow import workflow


def make_extraction(**overrides):
    """Build a valid Extraction with sane defaults, overriding only what a test cares about."""
    base = dict(intent="access_issue", urgency="normal", account_id="A-1001",
                requested_action="check my status", needs_human_review=False,
                missing_information=[], confidence=0.9)
    base.update(overrides)
    return Extraction(**base)


class FakeDrafterResult:
    """Stands in for whatever Runner.run(...) normally returns — only .final_output is used."""
    def __init__(self, text):
        self.final_output = text


@pytest.mark.asyncio
async def test_escalated_when_needs_human_review(monkeypatch):
    async def fake_extract(email):
        return make_extraction(needs_human_review=True)
    monkeypatch.setattr(workflow, "extract", fake_extract)

    result = await workflow.handle(EmailIn(message_id="msg-1", from_address="a@b.com",
                                            subject="s", body="please cancel my subscription"))
    assert result["status"] == "escalated"


@pytest.mark.asyncio
async def test_needs_information_when_account_id_missing(monkeypatch):
    async def fake_extract(email):
        return make_extraction(account_id=None, needs_human_review=False)
    monkeypatch.setattr(workflow, "extract", fake_extract)

    result = await workflow.handle(EmailIn(message_id="msg-2", from_address="a@b.com",
                                            subject="s", body="what's my account status?"))
    assert result["status"] == "needs_information"


@pytest.mark.asyncio
async def test_blocked_by_policy_when_draft_violates_rules(monkeypatch):
    async def fake_extract(email):
        return make_extraction(needs_human_review=False, account_id="A-1001")
    monkeypatch.setattr(workflow, "extract", fake_extract)

    async def fake_run(agent, prompt, max_turns=1):
        return FakeDrafterResult("Your refund has been issued.")   # a banned phrase, on purpose
    monkeypatch.setattr(workflow.Runner, "run", fake_run)

    result = await workflow.handle(EmailIn(message_id="msg-3", from_address="a@b.com",
                                            subject="s", body="where's my refund?"))
    assert result["status"] == "blocked_by_policy"


@pytest.mark.asyncio
async def test_awaiting_approval_on_a_clean_draft(monkeypatch):
    async def fake_extract(email):
        return make_extraction(needs_human_review=False, account_id="A-1001")
    monkeypatch.setattr(workflow, "extract", fake_extract)

    async def fake_run(agent, prompt, max_turns=1):
        return FakeDrafterResult("Thanks for reaching out — here's what I found on your account.")
    monkeypatch.setattr(workflow.Runner, "run", fake_run)

    result = await workflow.handle(EmailIn(message_id="msg-4", from_address="a@b.com",
                                            subject="s", body="what's my status?"))
    assert result["status"] == "awaiting_approval"