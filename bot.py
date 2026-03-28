import requests
import xml.etree.ElementTree as ET
import time
import os

URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/fiyat_v3.xml"

TARGET_MODEL = "1.8 Hybrid Flame X-Pack e-CVT"

def get_price():
    response = requests.get(URL)
    root = ET.fromstring(response.content)

    for item in root.findall(".//ModelFiyat"):
        model = item.find("Model")
        yil = item.find("ModelYili")
        price = item.find("KampanyaliFiyati2")

        if model is None or yil is None:
            continue

        model_text = model.text.strip()
        yil_text = yil.text.strip()

        if model_text == TARGET_MODEL and yil_text == "2026":
            if price is not None and price.text:
                return price.text.strip()

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

# 🔥 TEST MESAJI
send_telegram("Toyota bot aktif 🚀")

while True:
    try:
        price = get_price()
        print("Fiyat:", price)

        if price and last_price and price != last_price:
            msg = f"🚨 Toyota fiyat değişti!\nEski: {last_price}\nYeni: {price}"
            print(msg)
            send_telegram(msg)

        last_price = price
        time.sleep(300)

    except Exception as e:
        print("Hata:", e)
        time.sleep(60)
