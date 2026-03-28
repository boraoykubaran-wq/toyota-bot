import requests
import xml.etree.ElementTree as ET
import time

URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/fiyat_v3.xml"

def get_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = 'utf-8' # Türkçe karakterler için
        root = ET.fromstring(response.content)

        print("--- XML TARAMASI BAŞLADI ---")
        found_models = []

        for item in root.findall(".//ModelFiyat"):
            model = item.findtext("Model", "").strip()
            yil = item.findtext("ModelYili", "").strip()
            fiyat = item.findtext("KampanyaliFiyati2", "").strip()

            # Sadece "Flame" veya "Cross" geçenleri loga yaz ki kalabalık olmasın
            if "Flame" in model or
