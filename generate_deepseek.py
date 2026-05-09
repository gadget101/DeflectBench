import asyncio
from api.deepseek_client import call
from generate_core import run

MODEL = "deepseek-v4-pro"   

if __name__ == "__main__":
    asyncio.run(run(MODEL, call))
