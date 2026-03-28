import requests
import xml.etree.ElementTree as ET
import time
import os

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

        # XML içinde Corolla Cross Hybrid Flame'i arıyoruz
        for item in root.findall(".//ModelFiyat"):
            model = item.findtext("Model", "").strip()
            yil = item.findtext("ModelYili", "").strip()
            fiyat = item.findtext("KampanyaliFiyati2", "").strip()

            # 🎯 NOKTA ATIŞI FİLTRE
            m_up = model.upper()
            if "CROSS" in m_up and "FLAME" in m_up and "HYBRID" in m_up and yil == "2026":
                if fiyat and fiyat != "0":
                    return f"{model} ({yil})", fiyat
        return None, None
    except Exception as e:
        print(f"Veri çekme hatası: {e}")
        return None, None

# Başlangıçta botun çalıştığını sana haber verelim
send_telegram_msg("⚓️ Kaptan, Corolla Cross Takip Botu Railway üzerinde yayına girdi!")

last_saved_price = None

while True:
    model_adi, current_price = get_toyota_price()
    ts = time.strftime("%H:%M:%S")

    if current_price:
        print(f"[{ts}] Model: {model_adi} | Fiyat: {current_price}")
        
        # Fiyat ilk kez çekiliyorsa veya değişmişse mesaj at
        if last_saved_price is None:
            last_saved_price = current_price
            send_telegram_msg(f"✅ Takip Başladı!\n🚗 {model_adi}\n💰 Güncel Fiyat: {current_price}")
        
        elif current_price != last_saved_price:
            msg = f"🚨 FİYAT DEĞİŞTİ!\n🚗 {model_adi}\n📉 Eski: {last_saved_price}\n📈 Yeni: {current_price}"
            send_telegram_msg(msg)
            last_saved_price = current_price
    else:
        print(f"[{ts}] Aranan model şu an listede bulunamadı.")

    # 1 saatte bir kontrol et (Senin eski kodundaki gibi 3600 saniye)
    # Test aşamasında 600 (10 dk) yapabilirsin.
    time.sleep(3600)
