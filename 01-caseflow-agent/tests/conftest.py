import os

# The tests monkeypatch every model call, but importing caseflow.extract pulls in
# llm.py, which asserts these at import time. Set placeholders before collection
# so the import chain succeeds without a real key. setdefault means a real key in
# the environment still wins.
os.environ.setdefault("OPENAI_API_KEY", "not-used-tests-monkeypatch-the-model")
os.environ.setdefault("API_KEY", "not-used-tests-only")