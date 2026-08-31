from typing import Literal
from pydantic import BaseModel, Field

Intent = Literal["access_issue", "billing_question", "refund_status", "technical_issue", "other"]

class EmailIn(BaseModel):
    message_id: str = Field(min_length=3)
    from_address: str
    subject: str = ""
    body: str = Field(min_length=5)

class Extraction(BaseModel):
    intent: Intent
    urgency: Literal["low", "normal", "high"]
    account_id: str | None
    requested_action: str
    needs_human_review: bool
    missing_information: list[str]
    confidence: float = Field(ge=0.0, le=1.0)