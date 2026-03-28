import requests
import xml.etree.ElementTree as ET
import time

# 🔑 TELEGRAM BİLGİLERİN (Bunlar zaten doğru çalışıyor)
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
            model = item.findtext("Model", "").strip()
            yil = item.findtext("ModelYili", "").strip()
            # Toyota bazen fiyatı farklı etiketlere koyabiliyor, ikisine de bakalım
            fiyat = item.findtext("KampanyaliFiyati2", "").strip()
            if not fiyat or fiyat == "0":
                fiyat = item.findtext("OTVTesvikli1", "").strip()

            # 🎯 DAHA ESNEK FİLTRE:
            # Büyük/küçük harf duyarsız, "Cross" ve "Flame" kelimelerini arıyoruz.
            m_up = model.upper()
            if "CROSS" in m_up and "FLAME" in m_up:
                # 2026 veya 2025 modellerine bakıyoruz (Yıl geçiş dönemi olduğu için)
                if yil in ["2026", "2025"]:
                    if fiyat and fiyat != "0":
                        return f"{model} ({yil})", fiyat
        return None, None
    except Exception as e:
        print(f"Veri çekme hatası: {e}")
        return None, None

last_saved_price = None

# Railway başladığında sadece bir kez "Bağlantı Tamam" desin
print("⚓️ Bot Railway üzerinde çalışmaya başladı...")

while True:
    model_adi, current_price = get_toyota_price()
    ts = time.strftime("%H:%M:%S")

    if current_price:
        print(f"[{ts}] BAŞARILI! Model: {model_adi} | Fiyat: {current_price}")
        
        # Fiyat ilk kez çekiliyorsa veya bir değişim varsa Telegram at
        if last_saved_price is None or current_price != last_saved_price:
            msg = f"✅ Fiyat Yakalandı!\n🚗 {model_adi}\n💰 Güncel Fiyat: {current_price}"
            send_telegram_msg(msg)
            last_saved_price = current_price
    else:
        # Eğer hala bulunamıyorsa loglara "Bulunamadı" yazalım ama Telegram'ı meşgul etmeyelim
        print(f"[{ts}] Uyarı: Filtreye uygun araç XML listesinde henüz eşleşmedi.")

    # Test için süreyi 15 dakikaya (900 saniye) indirebilirsin
    time.sleep(3600)
