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

        for item in root.findall(".//ModelFiyat"):
            # XML Yapısına göre tam eşleme
            govde = (item.findtext("Govde") or "").strip()   # COROLLA CROSS
            model_tipi = (item.findtext("Model") or "").strip() # 1.8 Hybrid Flame e-CVT
            yil = (item.findtext("ModelYili") or "").strip()    # 2026
            fiyat = (item.findtext("KampanyaliFiyati2") or "").strip() # 2534000 TL

            # 🎯 FİLTRE: Govde "COROLLA CROSS" olacak ve Model içinde "Flame" geçecek
            if "CROSS" in govde.upper() and "FLAME" in model_tipi.upper():
                if yil == "2026" and fiyat:
                    return f"{govde} {model_tipi} ({yil})", fiyat
        
        return None, None
    except Exception as e:
        print(f"Hata: {e}")
        return None, None

last_saved_price = None

while True:
    full_name, current_price = get_toyota_price()
    ts = time.strftime("%H:%M:%S")

    if current_price:
        print(f"[{ts}] BAŞARILI: {full_name} -> {current_price}")
        
        if last_saved_price is None or current_price != last_saved_price:
            msg = f"✅ Fiyat Yakalandı!\n🚗 {full_name}\n💰 Kampanyalı: {current_price}"
            send_telegram_msg(msg)
            last_saved_price = current_price
    else:
        print(f"[{ts}] Model XML içinde bulunamadı.")

    # 1 saatte bir kontrol (3600 sn)
    time.sleep(3600)
