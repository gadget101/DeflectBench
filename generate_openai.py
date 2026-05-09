import asyncio
from api.openai_client import call
from generate_core import run

MODEL = "gpt-5.5"   

if __name__ == "__main__":
    asyncio.run(run(MODEL, call))
