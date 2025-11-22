# choco_sniper_pro.py
import asyncio
import random
import json
import httpx
from typing import Set
from urllib.parse import urlparse
from datetime import datetime

from playwright.async_api import async_playwright
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.responses import StreamingResponse
from contextlib import asynccontextmanager
import uvicorn

urls = [
    "https://secretsanta.cadbury.co.uk/code/a1008e92-b95d-4e13-a86e-fce60450ec7d",
    "https://secretsanta.cadbury.co.uk/code/76dd6a79-80db-40b2-957d-9658e7727d72",
    "https://secretsanta.cadbury.co.uk/code/4f8ed25b-2aeb-4986-9a30-08de1b353f4a",
    "https://secretsanta.cadbury.co.uk/code/2dd32a22-b8e6-40c6-e60d-08de1baaab95",
    "https://secretsanta.cadbury.co.uk/secretsanta/CfDJ8J-4L2JLEjBLsbt_V274SAuJTeQjpw-1Tzv8XqFJ3qdh5xkW817E3CQIpGYGq5zaygkRtuCU16Vdz3P4-pfzF-CM-aQJ-dtWQkFYPgOQlt2xS3jUxtwSiwS0rzG9ZJIAy5PAGWchU0r5",
    "https://secretsanta.cadbury.co.uk/code/e3759f5a-7b85-41ca-44c2-08de1c41764c",
    "https://secretsanta.cadbury.co.uk/code/311d9845-fce3-47ce-60f4-08de1c2c80de",
    "https://secretsanta.cadbury.co.uk/code/ec53918f-40d4-4794-d1a3-08dd1325334f",
    "https://secretsanta.cadbury.co.uk/code/c958f680-b052-4741-6546-08de1c2c80de",
    "https://secretsanta.cadbury.co.uk/code/e9157bb2-9890-4014-ac80-100d669ed362",
    "https://secretsanta.cadbury.co.uk/code/d1f53ad8-fa57-49fb-b7f0-fb110b8a812e",
    "https://secretsanta.cadbury.co.uk/secretsanta/CfDJ8J-4L2JLEjBLsbt_V274SAuz6j9GxI6MJ_SlwNHWwywFwDKpF0URDctiE9jnlfBSzWsTjAX7Uxqvg2ueEL4zmPI2JnJLKPLYSCHRe5JKCi5fusZ0me2pcm_bGHuZoJv3RZqakBvfWUSU?ar=False&codeId=CfDJ8J-4L2JLEjBLsbt_V274SAs5JMDu-XMsFN2RPxMMOAE9Kmnt7wDQ9s7hCPzvaKtPmnwtuulttWZMb0BhBZqriXME-wn0XpKXSDEhM2md50_JOEq-HwKnn9FTMJFYINsgeJxHYoD72B1O&utm_source=QR&utm_medium=QR_Code",
    "https://secretsanta.cadbury.co.uk/code/982cb88e-5764-462c-6f75-08de1d992242",
    "https://secretsanta.cadbury.co.uk/secretsanta/CfDJ8J-4L2JLEjBLsbt_V274SAthTLbuqJGombFSxRpxu2Jbty5idkvMITls-5-r-uwtJwWctvACr4U8b44sV1oCw8wYV0nBF4EBAr3g18GIcPobbXPOoSaqt9dZFDxerFpctcrgm0XOO-DJ",
    "https://secretsanta.cadbury.co.uk/code/63699f0c-b271-4055-85e2-08dcfdae2585",
    "https://secretsanta.cadbury.co.uk/code/631e209e-4a2b-4cc5-e280-08dcfdae24ce",
    "https://secretsanta.cadbury.co.uk/code/61d71f43-30ea-4685-8c1a-08dcfcd4f6a7",
    "https://secretsanta.cadbury.co.uk/code/7c019550-fa88-4260-94b0-ffaae170fbfd",
    "https://secretsanta.cadbury.co.uk/code/2693b6db-9274-4c66-b8ab-9f824d1afff5",
]

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/REPLACE_WITH_YOUR_WEBHOOK"

opened_destinations: Set[str] = set()
status_log: list = []
BAD_URL_CONTAINS = "missed-out"

async def send_discord_webhook(final_url: str):
    if not DISCORD_WEBHOOK or "REPLACE_WITH" in DISCORD_WEBHOOK:
        return
    embed = {
        "title": "CHOCOLATE SECURED!",
        "description": f"**New active link found!**\n{final_url}",
        "color": 0x9b59b6,
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {"text": "Cadbury Secret Santa Sniper Pro"},
    }
    payload = {"content": "@everyone FREE CHOCOLATE INCOMING!!!", "embeds": [embed]}
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            await client.post(DISCORD_WEBHOOK, json=payload)
        except Exception:
            pass

async def check_url_real_browser(url: str, page) -> str:
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)
        return page.url
    except Exception as e:
        return f"Error: {e}"

async def monitor_links():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="en-GB",
        )
        page = await context.new_page()

        while True:
            new_found_this_round = False
            for url in urls:
                final_url = await check_url_real_browser(url, page)

                entry = {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "url": url,
                    "final": final_url,
                    "status": "unknown"
                }

                if not final_url.startswith("http"):
                    entry["status"] = "error"
                elif BAD_URL_CONTAINS in final_url.lower():
                    entry["status"] = "missed"
                else:
                    normalized = urlparse(final_url)._replace(query="", fragment="").geturl()
                    if normalized not in opened_destinations:
                        entry["status"] = "SUCCESS"
                        opened_destinations.add(normalized)
                        new_found_this_round = True
                        await send_discord_webhook(final_url)
                    else:
                        entry["status"] = "already_opened"

                status_log.append(entry)
                if len(status_log) > 500:
                    status_log.pop(0)

            await asyncio.sleep(60 + random.randint(-15, 15))

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(monitor_links())
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1 style='color:#f59e0b;background:#0a0e27;padding:100px;text-align:center;'>Place index.html in /static folder</h1>"

@app.get("/events")
async def event_stream():
    async def generator():
        last_id = 0
        while True:
            if len(status_log) > last_id:
                yield f"data: {json.dumps(status_log[last_id:])}\n\n"
                last_id = len(status_log)
            await asyncio.sleep(0.5)
    return StreamingResponse(generator(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
