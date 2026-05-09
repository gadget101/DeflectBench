from dotenv import load_dotenv
load_dotenv()
 
import asyncio
import os
import aiohttp
 
API_KEY   = os.environ.get("OPENAI_API_KEY", "")
BASE_URL  = "https://api.openai.com/v1/chat/completions"
SEMAPHORE = asyncio.Semaphore(10)   
 
async def call(session: aiohttp.ClientSession, model: str, prompt: str,
               temperature: float = 1.0) -> dict:
    async with SEMAPHORE:
        payload = {
            "model":       model,
            "messages":    [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }
        headers = {"Authorization": f"Bearer {API_KEY}"}
        try:
            async with session.post(BASE_URL, headers=headers, json=payload) as resp:
                if resp.status == 429:
                    retry_after = int(resp.headers.get("Retry-After", 15))
                    await asyncio.sleep(retry_after)
                    return await call(session, model, prompt, temperature)  
                if resp.status != 200:
                    text = await resp.text()
                    return {"text": f"ERROR:{resp.status}:{text[:200]}", "input_tokens": 0, "output_tokens": 0}
                data = await resp.json()
                usage = data.get("usage", {})
                return {
                    "text":          data["choices"][0]["message"]["content"],
                    "input_tokens":  usage.get("prompt_tokens", 0),
                    "output_tokens": usage.get("completion_tokens", 0),
                }
        except Exception as e:
            return {"text": f"ERROR:exception:{str(e)[:200]}", "input_tokens": 0, "output_tokens": 0}