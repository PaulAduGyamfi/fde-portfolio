from fastapi import FastAPI
from .schemas import EmailIn, Extraction 
from .extract import extract

app = FastAPI(title="CaseFlow")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/extract", response_model=Extraction)
async def extract_email(email: EmailIn):
    return await extract(email)
