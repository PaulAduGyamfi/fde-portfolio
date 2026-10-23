Calibration check: inconclusive. Intent accuracy was 100% across all 20 cases, so there was no
variance in intent-correctness to test confidence against. Sample was also heavily skewed — 19/20
cases landed in the >=0.85 bucket, only 1 in 0.6-0.85, none below 0.6 — too small in the lower
buckets to draw any conclusion either way.


Separate finding, not calibration: confidence stayed at 0.98-0.99 on multiple cases (001, 003, 009,
010, 018) where urgency, needs_human_review, or account_id were wrong — including adversarial
cases. Confidence as currently defined only estimates intent correctness, and shouldn't be used as
a proxy for overall extraction trustworthiness.

-------------------

Iteration 3: moved account_id formatting out of the prompt into
normalize_account_id().

account_id 100%, now structural — the model doesn't format it, so it can't
regress. urgency and needs_human_review each gained one case, which is noise.

Hypothesis not supported. Intent stayed at 80%.

Better finding: iteration 2 failed intent on 005, 011, 012, 015. Iteration 3
failed on 002, 005, 011, 015. Same count, different set — 012 fixed, 002 broke,
no instruction change touching either. Only 011 and 015 fail in every run.

So intent carries about ±10 points of noise at n=20 — the same size as the
regression I was trying to explain. Iteration 2's drop may have been variance.
Single runs can't tell the difference.

Next: 3-5 runs per version, compare averages. Pin temperature lower first.

Side effect: the >=0.85 confidence bucket now reads 15/19 = 78.9% intent
accuracy. calibration_check read 19/19 and measured nothing. High confidence is
wrong about one time in five.