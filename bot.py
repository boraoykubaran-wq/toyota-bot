import requests
import xml.etree.ElementTree as ET
import time

URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/fiyat_v3.xml"

TARGET_MODEL = "1.8 Hybrid Flame X-Pack e-CVT"

def get_price():
    response = requests.get(URL)
    root = ET.fromstring(response.content)

    for item in root.findall(".//ModelFiyat"):
        model = item.find("Model")

        if model is not None and model.text.strip() == TARGET_MODEL:

            # Kampanyalı fiyat
            kampanya = item.find("KampanyaliFiyati2")
            if kampanya is not None and kampanya.text:
                return f"{model.text} → {kampanya.text}"

            # fallback
            otv = item.find("OTVTesvikli1")
            if otv is not None and otv.text:
                return f"{model.text} → {otv.text}"

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
