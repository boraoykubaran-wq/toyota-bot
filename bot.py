import os
import requests
import xml.etree.ElementTree as ET
import time

# 🔑 Değişkenleri Railway'den çekiyoruz
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/fiyat_v3.xml"

def send_telegram_msg(msg):
    if not TOKEN or not CHAT_ID: 
        print("HATA: Değişkenler eksik!")
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=15)
    except Exception as e:
        print(f"Hata: {e}")

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

            if "CROSS" in govde.upper() and "FLAME" in model.upper() and yil == "2026":
                return f"{govde} {model}", fiyat
        return None, None
    except Exception as e:
        print(f"Veri çekme sorunu: {e}")
        return None, None

# Başlangıçta None bırakıyoruz ki ilk bulduğu fiyatı bir kez bildirsin
last_saved_price = None

while True:
    model_adi, current_price = get_toyota_price()
    
    if current_price:
        if last_saved_price is None:
            # 🔔 BOT İLK KEZ ÇALIŞTIĞINDA BU MESAJI ATACAK
            send_telegram_msg(f"✅ Takip Başladı!\n🚗 {model_adi}\n💰 Güncel Fiyat: {current_price}")
            last_saved_price = current_price
            print(f"Takip başlatıldı: {current_price}")
            
        elif current_price != last_saved_price:
            # 🚨 SADECE FİYAT DEĞİŞTİĞİNDE BU MESAJI ATACAK
            send_telegram_msg(f"🚨 FİYAT DEĞİŞTİ!\n🚗 {model_adi}\n📉 Eski: {last_saved_price}\n📈 Yeni: {current_price}")
            last_saved_price = current_price
            print(f"Değişim algılandı: {current_price}")
    
    # 1 saatte bir kontrol (3600 saniye)
    time.sleep(3600)
