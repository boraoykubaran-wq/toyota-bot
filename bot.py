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
        
        # Tüm modelleri gez ve "Flame" veya "Hybrid" geçenleri ekrana bas
        for item in root.findall(".//ModelFiyat"):
            model = item.findtext("Model", "").strip()
            yil = item.findtext("ModelYili", "").strip()
            fiyat = item.findtext("KampanyaliFiyati2", "").strip()

            # Logları kirletmemek için sadece ilgili kelimeleri içerenleri basıyoruz
            if "Flame" in model or "Hybrid" in model or "Cross" in model:
                print(f"BULUNDU -> Model: [{model}] | Yıl: [{yil}] | Fiyat: [{fiyat}]")

                # Hedef filtremiz (Burayı loglara baktıktan sonra düzelteceğiz)
                if "Flame" in model and "Hybrid" in model and yil == "2026":
                    if fiyat and fiyat != "0":
                        return f"{model} ({yil}) -> {fiyat}"

        print("--- TARAMA BİTTİ ---")
        return "Eşleşen model bulunamadı, loglardaki isimleri kontrol et."

    except Exception as e:
        return f"Hata: {e}"

while True:
    price_info = get_price()
    print(f"Sonuç: {price_info}")
    time.sleep(300)
