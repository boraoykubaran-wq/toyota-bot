import requests
import xml.etree.ElementTree as ET
import time

URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/fiyat_v3.xml"

def get_price():
    response = requests.get(URL)
    root = ET.fromstring(response.content)

    for item in root.findall(".//ModelFiyat"):
        model = item.find("Model")
        yil = item.find("ModelYili")
        price = item.find("KampanyaliFiyati2")

        if model is not None and yil is not None and price is not None:

            model_text = model.text.strip()

            # 🔥 ESNEK ARAMA
            if "Hybrid Flame" in model_text and yil.text == "2026":

                if price.text:
                    return f"{model_text} → {price.text}"

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
