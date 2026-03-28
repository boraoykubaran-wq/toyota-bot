import requests
from bs4 import BeautifulSoup
import time
import os

URL = "https://www.sahibinden.com/oto360/sifir-araclar/toyota-corolla-cross-fiyat-listesi"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_price():
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text(separator="\n")
    lines = text.split("\n")

    for i, line in enumerate(lines):
        if "Corolla Cross SUV" in line:
            for j in range(i, i+5):
                if "TL" in lines[j]:
                    return lines[j].strip()

    return None


def send_telegram(msg):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    requests.post(url, data={
        "chat_id": chat_id,
        "text": msg
    })


last_price = None

# 🔥 TEST MESAJI (ilk çalışınca gönderir)
send_telegram("Bot çalıştı 🚀")

while True:
    try:
        price = get_price()
        print("Bulunan fiyat:", price)

        if price and last_price and price != last_price:
            msg = f"🚨 Fiyat değişti!\nEski: {last_price}\nYeni: {price}"
            print(msg)
            send_telegram(msg)

        last_price = price
        time.sleep(300)

    except Exception as e:
        print("Hata:", e)
        time.sleep(60)
