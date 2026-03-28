import requests
import xml.etree.ElementTree as ET
import time

URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/fiyat_v3.xml"

def get_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.content)

        print("\n--- [TARAMA BAŞLADI] ---")
        
        for item in root.findall(".//ModelFiyat"):
            model = item.findtext("Model", "").strip()
            yil = item.findtext("ModelYili", "").strip()
            # Kampanyalı fiyat (Ekran görüntüsündeki 2.534.000 TL genelde bu etikettedir)
            fiyat = item.findtext("KampanyaliFiyati2", "").strip()

            # 🎯 AKILLI FİLTRE: 
            # Hem "CROSS" hem "HYBRID" hem "FLAME" kelimeleri aynı satırda geçmeli
            model_upper = model.upper()
            if "CROSS" in model_upper and "FLAME" in model_upper and "HYBRID" in model_upper:
                # 2026 model yılı kontrolü
                if yil == "2026":
                    if fiyat and fiyat != "0":
                        print(f"✅ HEDEF BULUNDU: {model} -> {fiyat}")
                        return f"{model} ({yil}) -> {fiyat}"

        print("--- [EŞLEŞME BULUNAMADI - LOGLARI İNCELE] ---")
        return None

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

last_price = None

while True:
    price_info = get_price()
    current_time = time.strftime("%H:%M:%S")
    
    if price_info:
        print(f"[{current_time}] Güncel Fiyat: {price_info}")
        
        # Fiyat değişimi kontrolü
        if last_price and price_info != last_price:
            print("🚨 DİKKAT: FİYAT DEĞİŞTİ!")
        
        last_price = price_info
    else:
        print(f"[{current_time}] Aranan model henüz XML listesinde görülmedi.")

    # 5 dakikada bir kontrol (Railway için ideal süre)
    time.sleep(300)
