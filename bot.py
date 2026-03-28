import requests
import xml.etree.ElementTree as ET
import time

# Toyota Backend XML Linki
URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/fiyat_v3.xml"

def get_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    root = ET.fromstring(response.content)

    found_any = False
    
    for item in root.findall(".//ModelFiyat"):
        model = item.findtext("Model", "").strip()
        yil = item.findtext("ModelYili", "").strip()
        fiyat = item.findtext("KampanyaliFiyati2", "").strip()

        # Debug: En azından Flame geçen modelleri logda görelim ki neyi yanlış arıyoruz anlayalım
        if "Flame" in model:
            found_any = True
            # print(f"DEBUG: Bulunan -> {model} ({yil})") # Gerekirse açabilirsin

        # HEDEF FİLTRE: "Hybrid", "Flame" ve "2026" (Veya 2025 ise ona göre güncelle)
        if "Hybrid" in model and "Flame" in model and yil == "2026":
            if fiyat and fiyat != "0": # Fiyat etiketi doluysa döndür
                return f"{model} ({yil}) -> {fiyat}"

    if not found_any:
        return "Hata: Listede 'Flame' içeren hiçbir model bulunamadı."
    
    return "Filtreye uygun model bulundu ama fiyatı boş görünüyor."

last_price = None

while True:
    try:
        current_time = time.strftime("%H:%M:%S")
        price = get_price()
        print(f"[{current_time}] {price}")

        if last_price and price != last_price and "->" in str(price):
            print("🚨 FİYAT DEĞİŞTİ! (Alarm Çalıyor)")
            # Buraya ilerde Telegram kodu gelecek

        last_price = price
        time.sleep(300) # 5 dakikada bir kontrol

    except Exception as e:
        print(f"Hata oluştu: {e}")
        time.sleep(60)
