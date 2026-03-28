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
        data = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram hatası: {e}")

def get_toyota_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.content)

        print("\n--- [TARAMA BAŞLADI] ---")
        
        for item in root.findall(".//ModelFiyat"):
            # XML'deki hiyerarşiye tam uyum:
            govde = (item.findtext("Govde") or "").strip()       # "COROLLA CROSS"
            model_detay = (item.findtext("Model") or "").strip() # "1.8 Hybrid Flame e-CVT"
            yil = (item.findtext("ModelYili") or "").strip()     # "2026"
            fiyat = (item.findtext("KampanyaliFiyati2") or "").strip() # "2534000 TL"

            # 🎯 KRİTİK FİLTRE:
            # Gövde içinde "CROSS" ve model içinde "FLAME" geçmeli
            if "CROSS" in govde.upper() and "FLAME" in model_detay.upper():
                if yil == "2026" and fiyat:
                    full_name = f"{govde} {model_detay}"
                    return full_name, fiyat
        
        return None, None
    except Exception as e:
        print(f"Hata: {e}")
        return None, None

last_saved_price = None

while True:
    model_adi, current_price = get_toyota_price()
    ts = time.strftime("%H:%M:%S")

    if current_price:
        print(f"[{ts}] BAŞARILI: {model_adi} -> {current_price}")
        
        # Fiyat ilk kez çekiliyorsa veya değişmişse mesaj at
        if last_saved_price is None or current_price != last_saved_price:
            msg = f"✅ Fiyat Yakalandı!\n🚗 {model_adi} (2026)\n💰 Güncel: {current_price}"
            send_telegram_msg(msg)
            last_saved_price = current_price
    else:
        print(f"[{ts}] Model XML içinde bulunamadı. Filtreleri kontrol et.")

    # Railway'de logları takip etmek için 15 dakikada bir (900 sn)
    time.sleep(900)
