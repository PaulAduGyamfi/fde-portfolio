import json
from extractor import extract_ticket

FIELDS = ["intent", "customer_id", "urgency", "needs_human_review"]

def main():
    total = 0
    correct = {f: 0 for f in FIELDS}
    missing_pass = 0
    failures = []
    for line in open("cases.jsonl"):
        case = json.loads(line)
        actual = extract_ticket(case["text"]).model_dump()
        expected = case["expected"]
        total += 1
        row = []
        for f in FIELDS:
            if actual[f] == expected[f]:
                correct[f] += 1
            else:
                row.append(f"{f}: expected={expected[f]!r} actual={actual[f]!r}")
        expected_missing = set(expected["missing_information"])
        actual_missing = set(actual["missing_information"])
        if expected_missing.issubset(actual_missing):
            missing_pass += 1
        else:
            row.append(f"missing_information: expected at least {expected_missing}, got {actual_missing}")
        if row:
            failures.append((case["id"], case.get("tags", []), row))
    
    print(f"cases={total}")
    for f in FIELDS:
        print(f"{f}_accuracy={correct[f] / total:.1%}")
    print(f"missing_information_pass={missing_pass / total:.1%}\n\nFAILURES")
    for cid, tags, errs in failures:
        print(cid, tags, " | ".join(errs))

if __name__ == "__main__":
    main()