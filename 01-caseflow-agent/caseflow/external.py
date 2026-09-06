import asyncio, httpx

RETRYABLE = {408, 429, 500, 502, 503, 504}

async def fetch_json(url: str, attempts: int = 3, timeout: float = 5.0, client: httpx.AsyncClient | None = None) -> dict | list: 
    delay = 0.5
    no_client_provided = client is None
    if no_client_provided:
        client = httpx.AsyncClient(timeout=timeout)
    try:
        for i in range(attempts): 
            try:
                r = await client.get(url, headers={"Accept": "application/vnd.github+json"}) 
                r.raise_for_status()
                return r.json()
            except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
                status = getattr(getattr(e, "response", None), "status_code", None) 
                if status is not None and status not in RETRYABLE:
                    raise
                if i == attempts - 1:
                    raise
                await asyncio.sleep(delay); delay *= 2
    finally:
        if no_client_provided:
            await client.aclose()