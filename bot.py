import requests
import xml.etree.ElementTree as ET
import time

URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/fiyat_v3.xml"

def get_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    
    # Türkçe karakterler için encoding ayarı
    response.encoding = 'utf-8'
    root = ET.fromstring(response.content)

    all_models = []
    
    for item in root.findall(".//ModelFiyat"):
        model_text = item.findtext("Model", "").strip()
        yil_text = item.findtext("ModelYili", "").strip()
        fiyat_text = item.findtext("KampanyaliFiyati2", "").strip()
        
        # Loglarda görmek için listeye ekle
        if model_text:
            all_models.append(f"{model_text} ({yil_text})")

        # 🎯 ESNEK FİLTRE: 
        # "Hybrid" ve "Flame" geçsin, yıl 2026 olsun (Veya 2025 ise ona göre bak)
        if "Hybrid" in model_text and "Flame" in model_text:
            # Eğer Corolla Cross arıyorsan buraya 'and "Cross" in model_text' ekleyebilirsin
            if yil_text in ["2026", "2025"]: # Her iki yılı da kontrol et
                if fiyat_text and fiyat_text != "0":
                    return f"{model_text} ({yil_text}) -> {fiyat_text}"

    # Eğer hiçbir şey bulunamazsa loglara mevcut modellerden örnek bas
    print("--- SİSTEMDE BULUNAN BAZI MODELLER ---")
    for m in all_models[:10]: # İlk 10 tanesini göster
        print(f"Görünen: {m}")
    print("---------------------------------------")
    
    return "Aranan kriterde model/fiyat bulunamadı (Filtreleri kontrol et)."

last_price = None

while True:
    try:
        current_time = time.strftime("%H:%M:%S")
        price_info = get_price()
        print(f"[{current_time}] {price_info}")

        if last_price and price_info != last_price and "->" in str(price_info):
            print("🚨 FİYAT DEĞİŞİMİ TESPİT EDİLDİ!")

        last_price = price_info
        time.sleep(300) # 5 dakikada bir kontrol

    except Exception as e:
        print(f"Hata: {e}")
        time.sleep(60)
