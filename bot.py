import requests
from bs4 import BeautifulSoup
import time

URL = "https://www.sahibinden.com/oto360/sifir-araclar/toyota-corolla-cross-fiyat-listesi"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_price():
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text()

    lines = text.split("\n")

    for i, line in enumerate(lines):
        if "Hybrid Flame e-CVT" in line:

            # alt satırda fiyat var
            for j in range(i, i+5):
                if "TL" in lines[j]:
                    return f"{line.strip()} → {lines[j].strip()}"

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
