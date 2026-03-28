import requests
from bs4 import BeautifulSoup
import time

# Telegram Bilgileri
TOKEN = "8768272603:AAFTYPyzQQGnCGR1CRMGw58tEN_nQc-9FSE"
CHAT_ID = "8421945805"
URL = "https://www.sahibinden.com/oto360/sifir-araclar/toyota-corolla-cross-fiyat-listesi"

def send_telegram_msg(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg[:4000]})
    except Exception as e:
        print(f"Telegram hatası: {e}")

def get_sahibinden_price():
    # Sahibinden bot korumasını geçmek için gerçek bir bilgisayar gibi davranıyoruz
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        
        # 403 hatası, Sahibinden'in Railway'i engellediğini gösterir
        if response.status_code == 403:
            return "HATA 403: Sahibinden bot koruması (Cloudflare) Railway'i engelledi.", None
        elif response.status_code != 200:
            return f"HATA: Sunucu {response.status_code} kodu döndürdü.", None

        # Sayfa başarıyla açıldıysa içeriği analiz et
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Sayfadaki tüm metin bloklarını tarıyoruz
        for element in soup.find_all(['tr', 'li', 'div', 'span', 'p']):
            text = element.get_text(strip=True).replace("\n", " ").replace("\t", " ")
            text_lower = text.lower()
            
            # İçinde "Flame" ve fiyat belirten "TL" veya "₺" geçen ilk mantıklı uzunluktaki satırı al
            if "flame" in text_lower and ("tl" in text_lower or "₺" in text_lower):
                if len(text) < 150: # Tüm sayfayı tek parça okumasını önlemek için
                    return text, text

        return "HATA: Sayfa açıldı ama 'Flame' kelimesi içeren fiyat bulunamadı.", None

    except Exception as e:
        return f"HATA: Sistemsel sorun: {e}", None

last_saved_price = None

print("⚓️ Sahibinden Tarayıcı Botu Çalıştırıldı...")

while True:
    status_msg, current_price = get_sahibinden_price()
    ts = time.strftime("%H:%M:%S")

    if current_price:
        print(f"[{ts}] BAŞARILI: {current_price}")
        if last_saved_price != current_price:
            send_telegram_msg(f"✅ Sahibinden Fiyatı Yakalandı!\n🚗 {current_price}")
            last_saved_price = current_price
    else:
        print(f"[{ts}] {status_msg}")
        # Hata durumunu Telegram'a sadece bir kez gönder
        if last_saved_price != status_msg:
            send_telegram_msg(f"❌ Sahibinden Bot Raporu:\n{status_msg}")
            last_saved_price = status_msg

    time.sleep(600) # 10 dakikada bir kontrol
