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

def get_toyota_price_brute():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.content)

        print("\n--- [XML TARAMASI BAŞLADI] ---")
        
        for item in root.iter('ModelFiyat'):
            model = (item.findtext("Model") or "").strip()
            yil = (item.findtext("ModelYili") or "").strip()
            
            # 🎯 HEDEF ARAÇ KONTROLÜ (Daha esnek)
            m_up = model.upper()
            if "CROSS" in m_up and "FLAME" in m_up:
                # Olası tüm fiyat etiketlerini sırayla dene
                for tag in ["KampanyaliFiyati2", "OTVTesvikli1", "KampanyaliFiyati1", "ListeFiyati"]:
                    fiyat = (item.findtext(tag) or "").strip()
                    if fiyat and fiyat != "0" and len(fiyat) > 5: # Geçerli bir fiyat formatı mı?
                        print(f"✅ BULDUM! Model: {model} | Yıl: {yil} | Fiyat: {fiyat} ({tag})")
                        return f"{model} ({yil})", fiyat

        print("--- [EŞLEŞME YOK - FİLTREYE TAKILDI] ---")
        return None, None
    except Exception as e:
        print(f"Hata: {e}")
        return None, None

last_saved_price = None

while True:
    model_adi, current_price = get_toyota_price_brute()
    ts = time.strftime("%H:%M:%S")

    if current_price:
        if last_saved_price is None or current_price != last_saved_price:
            msg = f"✅ Fiyat Yakalandı!\n🚗 {model_adi}\n💰 Fiyat: {current_price} TL"
            send_telegram_msg(msg)
            last_saved_price = current_price
            print(f"[{ts}] Mesaj gönderildi: {current_price}")
    else:
        print(f"[{ts}] Filtre uyuşmadı veya XML'de veri yok.")

    # Railway'de logları görmek için 10 dakikada bir (600 saniye)
    time.sleep(600)
