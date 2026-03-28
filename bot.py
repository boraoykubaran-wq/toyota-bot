import requests
import xml.etree.ElementTree as ET
import time

# 🔑 TELEGRAM BİLGİLERİN
TOKEN = "8768272603:AAFTYPyzQQGnCGR1CRMGw58tEN_nQc-9FSE"
CHAT_ID = "8421945805"
URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/fiyat_v3.xml"

def send_telegram_msg(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

def get_toyota_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.content)

        for item in root.findall(".//ModelFiyat"):
            govde = (item.findtext("Govde") or "").strip()       # "COROLLA CROSS"
            model_detay = (item.findtext("Model") or "").strip() # "1.8 Hybrid Flame e-CVT"
            yil = (item.findtext("ModelYili") or "").strip()     # "2026"
            fiyat = (item.findtext("KampanyaliFiyati2") or "").strip() 

            if "CROSS" in govde.upper() and "FLAME" in model_detay.upper():
                if yil == "2026" and fiyat:
                    return f"{govde} {model_detay}", fiyat
        return None, None
    except:
        return None, None

# --- BAŞLANGIÇ AYARLARI ---
last_saved_price = None
print("⚓️ Bot aktif, ilk kontrol yapılıyor...")

while True:
    model_adi, current_price = get_toyota_price()
    
    if current_price:
        # Fiyat ilk kez alınıyorsa sadece hafızaya kaydet, mesaj atma (Sürekli mesajı engeller)
        if last_saved_price is None:
            last_saved_price = current_price
            print(f"İlk fiyat kaydedildi: {current_price}")
            # Opsiyonel: Botun düzgün çalıştığını anlamak için tek bir mesaj atabilirsin
            send_telegram_msg(f"✅ Takip Başladı!\n🚗 {model_adi}\n💰 Mevcut Fiyat: {current_price}")
        
        # Eğer fiyat daha önce kaydedilenden farklıysa mesaj at
        elif current_price != last_saved_price:
            msg = f"🚨 FİYAT DEĞİŞTİ!\n🚗 {model_adi}\n📉 Eski: {last_saved_price}\n📈 Yeni: {current_price}"
            send_telegram_msg(msg)
            last_saved_price = current_price
            print(f"Fiyat değişti: {current_price}")
    
    # Kontrol aralığı: 1 saat (3600 saniye)
    time.sleep(3600)
