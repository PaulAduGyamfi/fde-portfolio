from agents import Agent, Runner, function_tool
import sys; sys.path.append("../day2_structured_extraction"); 
import llm # noqa
import re

ACCOUNTS = {
    "C-42": {"name": "Jordan Lee", "plan": "Pro", "status": "active"}, 
    "C-77": {"name": "Sam Ortiz", "plan": "Basic", "status": "locked"}
    }
CASES = {
    "C-42": [{"case_id": "K-9", "status": "open", "topic": "refund"}], 
    "C-77": [{"case_id": "K-12", "status": "open", "topic": "login"}]
    }

CUSTOMER_ID = re.compile(r"\bC-\d+\b")

@function_tool
def get_account(customer_id: str):
    """
    Return the account record for a known customer ID.
    """
    return ACCOUNTS.get(customer_id, {"error": "customer_not_found"})

@function_tool
def list_open_cases(customer_id: str):
    """
    Return currently open support cases for a known customer ID.
    """
    return CASES.get(customer_id, [])

service_agent = Agent(
    name="ServiceOps Investigator",
    instructions=(
        "Investigate support requests. Use get_account or list_open_cases only when authoritative " 
        "account/case data is needed to answer. Do not call tools for greetings, general questions, or when "
        "the request lacks a usable customer ID. Never claim a write/action occurred or that you are capable of doing so;"
        "you have read-only tools. If information is missing, say what is needed."
    ),
    tools=[get_account, list_open_cases],
)

def investigate(text: str):
    return Runner.run_sync(service_agent, text, max_turns=6)

def handle_request(text: str) -> dict:
    lowered = text.lower()
    looks_account_specific = any(w in lowered for w in ["account", "customer", "refund", "open case", "status"])
    if looks_account_specific and not CUSTOMER_ID.search(text):
        return {
            "status": "needs_information", 
            "message": "Please provide the customer ID (for example C-42) before account data is accessed."
            }
    return {
        "status": "completed", 
        "message": investigate(text).final_output
        }

if __name__ == "__main__":
    r = investigate(sys.argv[1] if len(sys.argv) > 1 else "What plan is customer C-42 on?")
    print("FINAL:", r.final_output)
    for item in r.new_items:
        print(type(item).__name__, getattr(item, "raw_item", ""))