Calibration check: inconclusive. Intent accuracy was 100% across all 20 cases, so there was no
variance in intent-correctness to test confidence against. Sample was also heavily skewed — 19/20
cases landed in the >=0.85 bucket, only 1 in 0.6-0.85, none below 0.6 — too small in the lower
buckets to draw any conclusion either way.


Separate finding, not calibration: confidence stayed at 0.98-0.99 on multiple cases (001, 003, 009,
010, 018) where urgency, needs_human_review, or account_id were wrong — including adversarial
cases. Confidence as currently defined only estimates intent correctness, and shouldn't be used as
a proxy for overall extraction trustworthiness.