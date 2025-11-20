import asyncio
import random
import signal
import sys
import webbrowser
from typing import Set
from urllib.parse import urlparse, urljoin

from playwright.async_api import async_playwright

# === CONFIGURATION ===
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

opened_destinations: Set[str] = set()

BAD_URL_CONTAINS = "missed-out"

async def check_url_real_browser(url: str, page) -> str:
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        final_url = page.url
        return final_url
    except Exception as e:
        return f"Error: {e}"

async def monitor_links(interval: int = 60, jitter: int = 15):
    print("🎅 Cadbury Secret Santa monitor STARTED (using real browser)")
    print("Press Ctrl+C to stop.\n")

    def signal_handler():
        print("\n🛑 Stopping...")
        asyncio.get_event_loop().stop()

    signal.signal(signal.SIGINT, lambda s, f: signal_handler())

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="en-GB",
        )
        page = await context.new_page()

        while True:
            new_active_found = False

            for url in urls:
                print(f"Checking → {url}")
                final_url = await check_url_real_browser(url, page)

                if not final_url.startswith("http"):
                    print(f"  ⚠️ Failed: {final_url}")
                    continue

                if BAD_URL_CONTAINS in final_url.lower():
                    print(f"  ❌ Still missed out")
                    continue

                # Normalize by removing query strings for deduplication
                normalized = urlparse(final_url)._replace(query="").geturl()

                if normalized not in opened_destinations:
                    print(f"  ✅🎉 NEW ACTIVE LINK DETECTED!")
                    print(f"     → {final_url}")
                    webbrowser.open(final_url)
                    opened_destinations.add(normalized)
                    new_active_found = True
                else:
                    print(f"  🔁 Already opened before")

            if not new_active_found:
                print("  ⏳ No new active links found this round.")

            # Sleep with jitter
            sleep_time = interval + random.randint(-jitter, jitter)
            print(f"  😴 Sleeping {sleep_time} seconds...\n")
            await asyncio.sleep(sleep_time)

if __name__ == "__main__":
    asyncio.run(monitor_links(interval=60, jitter=15))


