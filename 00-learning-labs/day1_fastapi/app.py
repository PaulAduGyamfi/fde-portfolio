
from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="ServiceOps v0")

class Ticket(BaseModel):
    ticket_id: str = Field(min_length=3)
    customer_id: str = Field(min_length=3)
    subject: str = Field(min_length=3)
    body: str = Field(min_length=5)
    channel: Literal["email", "web"] = "email"

class TicketAccepted(BaseModel):
    ticket_id: str = Field(min_length=3)
    customer_id: str = Field(min_length=3)
    status: Literal["received"] = "received"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tickets", response_model=TicketAccepted)
def ticket_submission(ticket: Ticket):
    return TicketAccepted(
        ticket_id=ticket.ticket_id,
        customer_id=ticket.customer_id
    )