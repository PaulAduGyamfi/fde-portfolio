import os
from dotenv import load_dotenv

load_dotenv()

assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY missing from .env"
PROVIDER = os.getenv("LLM_PROVIDER", "openai")