import asyncio
import httpx
import pytest
from caseflow.external import fetch_json


def test_retries_on_503_then_succeeds():
    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        if calls["count"] < 2:
            return httpx.Response(503)
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    client = httpx.AsyncClient(transport=transport)

    result = asyncio.run(fetch_json("https://fake/import/github?owner=prepo=r", attempts=3, client=client))

    assert result == {"ok": True}
    assert calls["count"] == 2


def test_404_is_raised_immediately_with_no_retry():
    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    client = httpx.AsyncClient(transport=transport)

    with pytest.raises(httpx.HTTPStatusError):
        asyncio.run(fetch_json("https://fake/import/github?owner=prepo=r", attempts=3, client=client))

    assert calls["count"] == 1