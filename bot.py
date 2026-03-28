import asyncio
from playwright.async_api import async_playwright
import time
import os
import requests

URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/"

async def get_price():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(URL)

        # cookie kabul
        try:
            await page.click("text=Kabul et", timeout=3000)
        except:
            pass

        # Corolla Cross seç
        await page.click("text=Corolla Cross Hybrid")

        await page.wait_for_timeout(3000)

        # fiyatı çek
        content = await page.content()

        await browser.close()

        # basit parsing
        if "2.534.000 TL" in content:
            return "2.534.000 TL"

    return None


def send_telegram(msg):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": msg}
    )


last_price = None

while True:
    try:
        price = asyncio.run(get_price())
        print("Fiyat:", price)

        if price and last_price and price != last_price:
            send_telegram(f"🚨 Fiyat değişti: {price}")

        last_price = price
        time.sleep(300)

    except Exception as e:
        print("Hata:", e)
        time.sleep(60)
