import requests
import xml.etree.ElementTree as ET
import time

URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/fiyat_v3.xml"

def get_price():
    response = requests.get(URL)
    root = ET.fromstring(response.content)

    for item in root.findall(".//ModelFiyat"):
        text = "".join(item.itertext())

        # 🔥 direkt metin içinde ara
        if "Hybrid Flame X-Pack" in text and "2026" in text:

            # fiyatı yakala
            for child in item:
                if child.tag == "KampanyaliFiyati2" and child.text:
                    return f"{text.strip()} → {child.text}"

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
