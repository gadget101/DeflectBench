from dotenv import load_dotenv
load_dotenv()
 
import asyncio
import os
import aiohttp
 
API_KEY   = os.environ.get("ANTHROPIC_API_KEY", "")
BASE_URL  = "https://api.anthropic.com/v1/messages"
SEMAPHORE = asyncio.Semaphore(15)   
 

_MAX_TOKENS = 2048
 
async def call(session: aiohttp.ClientSession, model: str, prompt: str,
               temperature: float = 1.0) -> dict:
    async with SEMAPHORE:
        payload = {
            "model":      model,
            "max_tokens": _MAX_TOKENS,   
            "messages":   [{"role": "user", "content": prompt}],
        }
        headers = {
            "x-api-key":         API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type":      "application/json",
        }
        try:
            async with session.post(BASE_URL, headers=headers, json=payload) as resp:
                if resp.status == 429:
                    retry_after = int(resp.headers.get("Retry-After", 20))
                    await asyncio.sleep(retry_after)
                    return await call(session, model, prompt, temperature)  
                if resp.status != 200:
                    text = await resp.text()
                    return {"text": f"ERROR:{resp.status}:{text[:200]}", "input_tokens": 0, "output_tokens": 0}
                data = await resp.json()
                usage = data.get("usage", {})
                return {
                    "text":          data["content"][0]["text"],
                    "input_tokens":  usage.get("input_tokens", 0),
                    "output_tokens": usage.get("output_tokens", 0),
                }
        except Exception as e:
            return {"text": f"ERROR:exception:{str(e)[:200]}", "input_tokens": 0, "output_tokens": 0}
 
