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
        fiyat = item.find("KampanyaliFiyati2")

        if model is None or yil is None:
            continue

        model_text = model.text.strip()
        yil_text = yil.text.strip()

        # 🎯 DOĞRU FİLTRE
        if "Hybrid Flame X-Pack" in model_text and yil_text == "2026":

            if fiyat is not None and fiyat.text:
                return f"{model_text} → {fiyat.text}"

    return None


while True:
    try:
        price = get_price()
        print("Bulunan fiyat:", price)
        time.sleep(300)

    except Exception as e:
        print("Hata:", e)
        time.sleep(60)
