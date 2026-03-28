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
        for
