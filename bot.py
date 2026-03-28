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

def get_toyota_price_debug():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.content)

        print("\n--- [DETAYLI TARAMA BAŞLADI] ---")
        
        # Tüm alt elemanları (recursive) tarayalım
        for item in root.iter('ModelFiyat'):
            model = (item.findtext("Model") or "").strip()
            yil = (item.findtext("ModelYili") or "").strip()
            
            # Tüm olası fiyat etiketlerini kontrol edelim
            fiyat1 = (item.findtext("KampanyaliFiyati2") or "").strip()
            fiyat2 = (item.findtext("OTVTesvikli1") or "").strip()
            fiyat3 = (item.findtext("ListeFiyati") or "").strip()
            
            final_price = fiyat1 if (fiyat1 and fiyat1 != "0") else (fiyat2 if (fiyat2 and fiyat2 != "0") else fiyat3)

            # Loglarda ne gördüğümüzü görelim
            if "CROSS" in model.upper() and "FLAME" in model.upper():
                print(f"EŞLEŞME: {model} | Yıl: {yil} | Fiyat: {final_price}")
                if final_price and final_price != "0":
                    return f"{model} ({yil})", final_price

        print("--- [TARAMA BİTTİ - EŞLEŞME YOK] ---\n")
        return None, None
    except Exception as e:
        print(f"Hata: {e}")
        return None, None

last_saved_price = None

while True:
    model_adi, current_price = get_toyota_price_debug()
    ts = time.strftime("%H:%M:%S")

    if current_price:
        print(f"[{ts}] BAŞARILI: {model_adi} -> {current_price}")
        if last_saved_price is None or current_price != last_saved_price:
            msg = f"✅ Fiyat Yakalandı!\n🚗 {model_adi}\n💰 Fiyat: {current_price} TL"
            send_telegram_msg(msg)
            last_saved_price = current_price
    else:
        print(f"[{ts}] Aranan model (Cross Flame) hala bulunamadı. Filtreleri genişletiyoruz...")
        # Eğer hiç bulamazsa loglara bilgi verelim
        
    # Railway'de logları hızlı görmek için süreyi şimdilik 10 dakikaya (600 sn) çekelim
    time.sleep(600)
