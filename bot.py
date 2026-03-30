import requests
import time
import json
import re

BOT_TOKEN = "BOT_TOKEN"
CHAT_ID = "CHAT_ID"

URL = "https://www.toyota.com.tr/araba-modelleri/corolla-cross-hybrid"


def get_price():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

        # SADECE "Başlangıç fiyatı" kısmını yakala
        match = re.search(
            r"Başlangıç fiyatı.*?([\d\.]+)\s*TL",
            r.text,
            re.DOTALL
        )

        if match:
            price = match.group(1)
            print("FOUND:", price)
            return price.replace(".", "")

    except Exception as e:
        print("HATA:", e)

    return None


def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )


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

        time.sleep(300)


if __name__ == "__main__":
    main()
