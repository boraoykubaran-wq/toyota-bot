import requests
from bs4 import BeautifulSoup
import time
import json

BOT_TOKEN = "TOKEN"
CHAT_ID = "CHAT_ID"

URL = "https://www.cetas.com.tr/toyota/yeni-toyota-corolla-cross"


def get_price():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")

        import re
        text = soup.get_text()

        match = re.search(r"Başlangıç Fiyatı.*?([\d\.]+)\s*TL", text)

        if match:
            return match.group(1).replace(".", "")

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
