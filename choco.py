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
    "https://secretsanta.cadbury.co.uk/secretsanta/CfDJ8J-4L2JLEjBLsbt_V274SAuJTeQjpw-1Tzv8XqFJ3qdh5xkW817E3CQIpGYGq5zaygkRtuCU16Vdz3P4-pfzF-CM-aQJ-dtWQkFYPgOQlt2xS3jUxtwSiwS0rzG9ZJIAy5PAGWchU0r5?ar=False&codeId=CfDJ8J-4L2JLEjBLsbt_V274SAtz6ScbT6BpacrMB0qlq1fYciA605It0dO3Et7bFTDCtXsb9bj4Wl8NZVVyr-wtlG7eHLNAOJdvxxvkx8bD5Bwy54cp3u7NGZJSH0GzwADiQlB1TK7D93Sc&utm_source=QR&utm_medium=QR_Code&utm_campaign=SecretSanta2025&utm_content=QRcode_Campaign_Scan&QR_product=North%20WestUK&QR_country=UK&QR_retail=none",
    "https://secretsanta.cadbury.co.uk/code/e3759f5a-7b85-41ca-44c2-08de1c41764c",
    "https://secretsanta.cadbury.co.uk/code/311d9845-fce3-47ce-60f4-08de1c2c80de",
    "https://secretsanta.cadbury.co.uk/code/ec53918f-40d4-4794-d1a3-08dd1325334f",
    "https://secretsanta.cadbury.co.uk/code/c958f680-b052-4741-6546-08de1c2c80de",
    "https://secretsanta.cadbury.co.uk/code/e9157bb2-9890-4014-ac80-100d669ed362",
    "https://secretsanta.cadbury.co.uk/code/d1f53ad8-fa57-49fb-b7f0-fb110b8a812e",
    "https://secretsanta.cadbury.co.uk/secretsanta/CfDJ8J-4L2JLEjBLsbt_V274SAuz6j9GxI6MJ_SlwNHWwywFwDKpF0URDctiE9jnlfBSzWsTjAX7Uxqvg2ueEL4zmPI2JnJLKPLYSCHRe5JKCi5fusZ0me2pcm_bGHuZoJv3RZqakBvfWUSU?ar=False&codeId=CfDJ8J-4L2JLEjBLsbt_V274SAs5JMDu-XMsFN2RPxMMOAE9Kmnt7wDQ9s7hCPzvaKtPmnwtuulttWZMb0BhBZqriXME-wn0XpKXSDEhM2md50_JOEq-HwKnn9FTMJFYINsgeJxHYoD72B1O&utm_source=QR&utm_medium=QR_Code&utm_campaign=SecretSanta2025&utm_content=QRcode_Campaign_Scan&QR_product=Greater%20LondonUK&QR_country=UK&QR_retail=none",
    "https://secretsanta.cadbury.co.uk/code/982cb88e-5764-462c-6f75-08de1d992242",
    "https://secretsanta.cadbury.co.uk/code/31ebc814-7b74-424e-4faf-08de1d9922c6",
    "https://secretsanta.cadbury.co.uk/secretsanta/CfDJ8J-4L2JLEjBLsbt_V274SAvCnm_OmjD7fpS0BtgP_cDEcxyijp3662egxW_l-QmLqjYQ0pH7Q7Qiq63NlUqkuUv_1g_0sCDXiXfbEYk-M8qJlWVC9QiaV9qWKAxPuusb-ATGyYQcMzQC?ar=False&codeId=CfDJ8J-4L2JLEjBLsbt_V274SAtTOiCQB4ndjyK4gvwHnjkN1lwA032f2pzt4Qa_RSl3DZ0jRa_tsPZLIyqM6L1WPP8h_8-qTLzp6hZd2CsoXuT8JQO-FgUU8Ixa5G5aTSxRHrTHkGO04gWA&utm_source=QR&utm_medium=QR_Code&utm_campaign=SecretSanta2025&utm_content=QRcode_Campaign_Scan&QR_product=Greater%20LondonUK&QR_country=UK&QR_retail=none",
    "https://secretsanta.cadbury.co.uk/code/d4a02842-7a37-4b16-291c-08de2100dc4b",
    "https://secretsanta.cadbury.co.uk/code/928038c9-8fcf-41e2-e6de-08de21c5d054",
    "https://secretsanta.cadbury.co.uk/code/bac40653-60f3-4fbc-e6c0-08de21c5d054",
    "https://secretsanta.cadbury.co.uk/code/e7de8f02-33b6-4271-b177-684d38a73499",
    "https://secretsanta.cadbury.co.uk/code/ce166a11-3146-497b-4236-08de21c5d055",
    "https://secretsanta.cadbury.co.uk/code/ccd1d633-8de0-4f43-824e-08de22b4fbb3",
    "https://secretsanta.cadbury.co.uk/code/f5a0a935-09de-4a23-d833-08de22b50f9b",
    "https://secretsanta.cadbury.co.uk/code/414a2eb9-a40c-4e73-54be-08de229fbfe5",
    "https://secretsanta.cadbury.co.uk/secretsanta/CfDJ8J-4L2JLEjBLsbt_V274SAv2D8-YV81Km-EXR50fCCl7ugfU-zFB6IYbRalUON5peb9zcbP1m1AR1kzHDwRlEHMhUXlV5lbgv0hSRjOv-eghnNo_nrdR6KpdlQZHGM-B3E01kFWFEMot?ar=False&codeId=CfDJ8J-4L2JLEjBLsbt_V274SAt2A7KSCrkw3RD5C2Pk6de6CFneDbhRKZX-J6vRtSWyEovDWWzPVxxTywAVvYaDDbm7wfacyrzuJ5hhiyO52iKT49zovZop8MbHf7gfscs4KN5LotpOmsyk&utm_source=QR&utm_medium=QR_Code&utm_campaign=SecretSanta2025&utm_content=QRcode_Campaign_Scan&QR_product=Greater%20LondonUK&QR_country=UK&QR_retail=none",
    "https://secretsanta.cadbury.co.uk/code/567cbe82-727a-4933-1f8e-08de23abf8f0",
    "https://secretsanta.cadbury.co.uk/code/a41e0362-4daa-438d-76c7-08de25815938",
    "https://secretsanta.cadbury.co.uk/code/984b39c8-aba1-4764-a3e3-08de2756bdd8NTmjRaLcfxMLLheUfSZwoFsJtgjMkm1a0KXv80LWw-OSrm1A9w?ar=False&codeId=CfDJ8J-4L2JLEjBLsbt_V274SAuwl1djkx2Q-LHo3QlmPkGCuhQKUIgF6YI0rJJLlYZjpTWWmJWNA2f2r-JcfbU2GRyoDOIlWlgUaTTU7YHud8KLo3TtvEuDYe8VRXpZle01SXNwInqMA_c6&utm_source=QR&utm_medium=QR_Code&utm_campaign=SecretSanta2025&utm_content=QRcode_Campaign_Scan&QR_product=Greater%20LondonUK&QR_country=UK&QR_retail=none&fbclid=Iwb21leAOKiGVjbGNrA4qIY2V4dG4DYWVtAjExAHNydGMGYXBwX2lkDDM1MDY4NTUzMTcyOAABHjfI_q6ikS1BZ3Nw7RfhhLPUBFS6fu3rHMJxBEaN3Ij74D7kpYNFRacDBSAi_aem_jdrmNQQ_hrCtRcfizTdHPg",
    "https://secretsanta.cadbury.co.uk/code/8f308ea2-9a1c-4094-394b-08de2756bd14",
    "https://secretsanta.cadbury.co.uk/code/240e8fe1-ff2a-43a4-8937-7acd2b85baae",
    "https://secretsanta.cadbury.co.uk/code/2eeac06f-e594-400c-85a9-08de28e4e758",
    "https://secretsanta.cadbury.co.uk/code/33646dc9-0148-46fd-f89d-08de28dc814b",
    "https://secretsanta.cadbury.co.uk/code/58e239d7-41e5-4bbd-7f8b-08de2b9c97c6",
    "https://secretsanta.cadbury.co.uk/code/4f0fbabb-fc89-4ec5-f1d9-08de2ec9a465",
    "https://secretsanta.cadbury.co.uk/code/8d0ad2e0-99e9-48d9-a854-6dc0263f2a8c",
    "https://secretsanta.cadbury.co.uk/code/e283d7eb-99e1-4ee9-84e6-08de3107ce91",
    "https://secretsanta.cadbury.co.uk/code/3fa8bedc-04a9-4d4b-576e-08de3107d04d",
    "https://secretsanta.cadbury.co.uk/code/3a5f4684-bc16-40b7-1d10-08de3107cf90",
    "https://secretsanta.cadbury.co.uk/code/79eab9a7-bbfb-4c92-90d8-f8da363bba1e",
    "https://secretsanta.cadbury.co.uk/code/21c076a9-6933-4014-0f82-08de3107cf90",
    "https://secretsanta.cadbury.co.uk/code/5b090654-0862-4760-b785-272f23972e21",
    "https://secretsanta.cadbury.co.uk/code/7375a354-c20d-4614-999a-9f729d56f1e8",
    "https://secretsanta.cadbury.co.uk/code/5c8e450c-d95d-4e9d-823e-14c09cfe97b1",
    "https://secretsanta.cadbury.co.uk/code/785dcae9-543c-4614-8160-689afc767b6c",
    "https://secretsanta.cadbury.co.uk/code/84d470af-719f-40dd-5da3-08de33f1cdcb",
    "https://secretsanta.cadbury.co.uk/code/4cba7ddc-03c3-4d6e-4279-08de334e5e59",
    "https://secretsanta.cadbury.co.uk/code/3cca1e64-2173-4671-778d-08de347c1720",
    "https://secretsanta.cadbury.co.uk/code/e7ba3539-1f59-4e44-8e15-930784154d5a",
    "https://secretsanta.cadbury.co.uk/code/29f82f90-dfd4-4262-5db4-08de34e0aad6",
    "https://secretsanta.cadbury.co.uk/code/b48e826a-f56d-4663-0076-08de347c1721",
    "https://secretsanta.cadbury.co.uk/code/5daa721b-f600-4980-8ac6-48d5fbedfc03",
    "https://secretsanta.cadbury.co.uk/code/4cd46228-0084-47ac-0bd2-08de358420b1",
    "https://secretsanta.cadbury.co.uk/code/29711680-e1c4-4d92-043c-08de3551ce2b",
    "https://secretsanta.cadbury.co.uk/code/5158b051-a721-42bd-87fe-08de367b5e7b",
    "https://secretsanta.cadbury.co.uk/code/4f6203e0-06cb-40d1-31b3-08de367b5d31",
    "https://secretsanta.cadbury.co.uk/code/529f24a5-2533-4d37-4450-08de367b5d31",
    "https://secretsanta.cadbury.co.uk/code/d65a5f51-42b1-4a93-6887-08de34a602f4",
    "https://secretsanta.cadbury.co.uk/code/fc32604c-a2bc-4c70-c8c9-08de36ba3e32",
    "https://secretsanta.cadbury.co.uk/code/2adc7c47-b456-467c-886f-2b70d38156de",
    "https://secretsanta.cadbury.co.uk/code/e5f69075-45f2-4d8e-bc22-08de37d30e5a",
    "https://secretsanta.cadbury.co.uk/code/ccb332ab-f4eb-45ff-3f15-08de37d30e5b",
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


