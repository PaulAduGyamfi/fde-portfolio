import uuid
import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends, HTTPException, Header
from .schemas import EmailIn, Extraction 
from .extract import extract, extract_github_issue
from .external import fetch_json


app = FastAPI(title="CaseFlow")

assert os.getenv("API_KEY"), "API_KEY missing from .env"
API_KEY = os.getenv("API_KEY")

def require_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status=401, detail="invalid api key")

@app.middleware("http")
async def add_run_id(request: Request, call_next):
    run_id = str(uuid.uuid4())
    request.state.run_id = run_id
    response = await call_next(request)
    response.headers["X-Run-Id"] = run_id
    return response

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/extract", response_model=Extraction, dependencies=[Depends(require_api_key)])
async def extract_email(email: EmailIn):
    return await extract(email)

@app.get("/import/github")
async def import_github(owner: str, repo: str):
    issues = await fetch_json(f"https://api.github.com/repos/{owner}/{repo}/issues")
    results = await asyncio.gather(*[extract_github_issue(issue) for issue in issues[:5]])
    return results
