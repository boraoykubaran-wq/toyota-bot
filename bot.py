import os
import requests
import xml.etree.ElementTree as ET
import time

# Değişkenleri Railway'den (Shared Variables) çekiyoruz
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/fiyat_v3.xml"

def send_telegram_msg(msg):
    if not TOKEN or not CHAT_ID: return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except:
        pass

def get_toyota_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.content)
        
        for item in root.findall(".//ModelFiyat"):
            govde = (item.findtext("Govde") or "").strip()
            model = (item.findtext("Model") or "").strip()
            yil = (item.findtext("ModelYili") or "").strip()
            fiyat = (item.findtext("KampanyaliFiyati2") or "").strip()

            # Tam hedefleme: Corolla Cross, Flame ve 2026 model
            if "CROSS" in govde.upper() and "FLAME" in model.upper() and yil == "2026":
                return f"{govde} {model}", fiyat
        return None, None
    except:
        return None, None

# Başlangıçta bildirim atmaması için mevcut fiyatı sabitliyoruz
last_saved_price = "2534000 TL"

while True:
    model_adi, current_price = get_toyota_price()
    
    # Sadece fiyat değişirse mesaj at
    if current_price and current_price != last_saved_price:
        msg = f"🚨 Fiyat Değişti!\n🚗 {model_adi}\n💰 Yeni Fiyat: {current_price}"
        send_telegram_msg(msg)
        last_saved_price = current_price
    
    # 1 saatte bir kontrol (3600 saniye)
    time.sleep(
