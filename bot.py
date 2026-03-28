import requests
import xml.etree.ElementTree as ET
import time

URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/fiyat_v3.xml"

def get_price():
    response = requests.get(URL)
    root = ET.fromstring(response.content)

    for item in root.findall(".//ModelFiyat"):
        model = item.find("Model")
        price = item.find("KampanyaliFiyati2")

        if model is not None and price is not None:
            if "Flame" in model.text and "Hybrid" in model.text:
                return f"{model.text} → {price.text}"

    return None


last_price = None

while True:
    try:
        price = get_price()
        print("Bulunan:", price)

        if last_price and price != last_price:
            print("🚨 FİYAT DEĞİŞTİ!")

        last_price = price
        time.sleep(300)

    except Exception as e:
        print("Hata:", e)
        time.sleep(60)
