import asyncio, json, sys 
sys.path.append("..")
from caseflow.schemas import EmailIn 
from caseflow.extract import extract

FIELDS = ["intent", "urgency", "account_id", "needs_human_review"]
sem = asyncio.Semaphore(4)

async def run_case(case):
    async with sem:
        out = await extract(EmailIn(**case["input"])) 
        return case, out.model_dump()

async def main():
    cases = [json.loads(l) for l in open("cases.jsonl")]
    results = await asyncio.gather(*[run_case(c) for c in cases]) 
    correct = {f: 0 for f in FIELDS}; failures = []
    for case, actual in results:
        exp = case["expected"]; row = [] 
        for f in FIELDS:
            if actual[f] == exp[f]: correct[f] += 1
            else: row.append(f"{f}: expected={exp[f]!r} actual={actual[f]!r}")
        if not set(exp["missing_information"]).issubset(set(actual["missing_information"])):
            row.append("missing_information incomplete")
        if row: failures.append((case["id"], case["tags"], actual["confidence"], row)) 
    n = len(cases)
    print(f"cases={n}")
    for f in FIELDS: print(f"{f}_accuracy={correct[f]/n:.1%}") 
    print("\nFAILURES (id, tags, confidence)")
    for f in failures: print(*f)


asyncio.run(main())