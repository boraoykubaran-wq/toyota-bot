import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 🔑 Değişkenleri Railway'den çekiyoruz
TOKEN = os.getenv("BOT_TOKEN", "8768272603:AAFTYPyzQQGnCGR1CRMGw58tEN_nQc-9FSE")
CHAT_ID = os.getenv("CHAT_ID", "8421945805")
URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/"

def send_message(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=15)
    except:
        pass

def get_price():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 20)
        
        driver.get(URL)
        time.sleep(5)

        # Çerezleri Kabul Et
        try:
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Tümüne izin ver')]")))
            btn.click()
        except:
            pass

        # Corolla Cross Linkini Bul ve Git
        links = driver.find_elements(By.TAG_NAME, "a")
        target_link = next((l.get_attribute("href") for l in links if l.get_attribute("href") and "corolla-cross" in l.get_attribute("href").lower()), None)

        if not target_link:
            driver.quit()
            return None

        driver.get(target_link)
        time.sleep(7)

        # Sayfa metnini al ve fiyatı ara
        body_text = driver.find_element(By.TAG_NAME, "body").text
        driver.quit()
        
        for line in body_text.split("\n"):
            # Özellikle 2026 ve Flame kelimelerini içeren satırı bul
            if "Flame" in line and ("2.534" in line or "TL" in line):
                return line
        return None
    except Exception as e:
        print(f"Hata: {e}")
        return None

# --- 🔁 ANA DÖNGÜ ---

# Başlangıçta None yapıyoruz ki ilk açılışta o meşhur mesaj gelsin
old_price = None

while True:
    print(f"[{time.strftime('%H:%M:%S')}] Kontrol ediliyor...")
    new_price = get_price()
    
    if new_price:
        # İlk kez çalışıyorsa fiyatı raporla
        if old_price is None:
            send_message(f"✅ Takip Başladı!\n🚗 {new_price}")
            old_price = new_price
        # Fiyat değişmişse bildir
        elif new_price != old_price:
            send_message(f"🚨 FİYAT DEĞİŞTİ!\n📉 Eski: {old_price}\n📈 Yeni: {new_price}")
            old_price = new_price
    
    # Yarım kalan parantez burada düzeltildi:
    time.sleep(1800)
