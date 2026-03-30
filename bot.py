import requests
from bs4 import BeautifulSoup
import time
import json

# TELEGRAM
BOT_TOKEN = "BOT_TOKENIN"
CHAT_ID = "CHAT_ID"

URL = "https://www.cetas.com.tr/toyota/yeni-toyota-corolla-cross"

def get_price():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # Sayfada "Başlangıç Fiyatı" yazan kısmı bul
    text = soup.get_text()

    import re
    match = re.search(r"Başlangıç Fiyatı.*?([\d\.]+)\s*TL", text)

    if match:
        return match.group(1).replace(".", "")
    
    return None


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)


def load_last_price():
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
        current_price = get_price()
        last_price = load_last_price()

        print("Current:", current_price, "Last:", last_price)

        if current_price:
            if last_price is None:
                save_price(current_price)

            elif current_price != last_price:
                send_telegram(f"🚗 Corolla Cross fiyat değişti!\n\nEski: {last_price} TL\nYeni: {current_price} TL")
                save_price(current_price)

        time.sleep(600)  # 10 dk


if __name__ == "__main__":
    main()
