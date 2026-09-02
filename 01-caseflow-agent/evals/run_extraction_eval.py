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

    
    buckets = {"<0.6": [0, 0], "0.6-0.85": [0, 0], ">=0.85": [0, 0]}

    def bucket_for(confidence):
        if confidence < 0.6:
            return "<0.6"
        elif confidence < 0.85:
            return "0.6-0.85"
        else:
            return ">=0.85"

    for case, actual in results:
        exp = case["expected"]
        b = bucket_for(actual["confidence"])
        buckets[b][1] += 1                          
        if actual["intent"] == exp["intent"]:
            buckets[b][0] += 1                       

    print("\nCALIBRATION (intent accuracy by confidence bucket)")
    for name, (correct, total) in buckets.items():
        if total == 0:
            print(f"{name}: no cases")
        else:
            print(f"{name}: {correct}/{total} = {correct/total:.1%}")

asyncio.run(main())