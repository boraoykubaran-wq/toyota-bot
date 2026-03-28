import requests
from bs4 import BeautifulSoup
import time

URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_price():
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text()

    lines = text.split("\n")

    for line in lines:
        if "Corolla Cross Hybrid" in line and "Flame" in line:
            return line.strip()

    return None


last_price = None

while True:
    try:
        price = get_price()
        print("Bulunan fiyat:", price)

        if last_price and price != last_price:
            print("🚨 FİYAT DEĞİŞTİ!")

        last_price = price
        time.sleep(300)

    except Exception as e:
        print("Hata:", e)
        time.sleep(60)
