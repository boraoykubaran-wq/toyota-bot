from playwright.sync_api import sync_playwright
import requests
import time
import json
import re

BOT_TOKEN = "BOT_TOKEN"
CHAT_ID = "CHAT_ID"

URL = "https://www.toyota.com.tr/araba-modelleri/suv-araclar"


def get_price():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(URL, timeout=60000)

            # sayfanın yüklenmesini bekle
            page.wait_for_timeout(5000)

            content = page.content()

            browser.close()

            matches = re.findall(r"\d{1,3}(?:\.\d{3})+\s*TL", content)

            print("FOUND:", matches)

            if matches:
                return matches[0].replace(".", "").replace(" TL", "")

    except Exception as e:
        print("HATA:", e)

    return None


def send_telegram(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
    except Exception as e:
        print("Telegram hata:", e)


def load_price():
    try:
        with open("price.json", "r") as f:
            return json.load(f)["price"]
    except:
        return None


def save_price(price):
    with open("price.json", "w") as f:
        json.dump({"price": price}, f)


def main():
    while True:
        current = get_price()
        last = load_price()

        print("Current:", current, "Last:", last)

        if current:
            if not last:
                save_price(current)

            elif current != last:
                send_telegram(
                    f"🚗 Corolla Cross fiyat değişti!\n\nEski: {last} TL\nYeni: {current} TL"
                )
                save_price(current)

        time.sleep(300)  # 5 dakika


if __name__ == "__main__":
    main()
