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

# 🔑 Değişkenler
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
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 25)
        
        driver.get(URL)
        time.sleep(8) # Sayfanın yüklenmesi için biraz daha süre

        # Çerez kabul butonunu dene
        try:
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Tümüne izin ver')]")))
            btn.click()
        except:
            pass

        # Corolla Cross Linkine Git
        links = driver.find_elements(By.TAG_NAME, "a")
        target_link = next((l.get_attribute("href") for l in links if l.get_attribute("href") and "corolla-cross" in l.get_attribute("href").lower()), None)

        if not target_link:
            return None

        driver.get(target_link)
        time.sleep(8)

        body_text = driver.find_element(By.TAG_NAME, "body").text
        
        for line in body_text.split("\n"):
            if "Flame" in line and ("2.534" in line or "TL" in line):
                return line
        return None
    except Exception as e:
        print(f"Hata: {e}")
        return None
    finally:
        if driver:
            driver.quit()

# --- 🔁 ANA DÖNGÜ ---

# Bilinen fiyatı peşin yazıyoruz ki gereksiz mesaj atmasın
old_price = "2.534.000 TL" 

while True:
    print(f"[{time.strftime('%H:%M:%S')}] Kontrol ediliyor...")
    new_price = get_price()
    
    # Sadece fiyat değişirse (indirim/zam) veya ilk kontrolde fiyat farklıysa mesaj atar
    if new_price and new_price != old_price:
        send_message(f"🔔 Corolla Cross Fiyat Güncellemesi:\n💰 {new_price}")
        old_price = new_price
        print(f"Yeni Fiyat Bildirildi: {new_price}")
    
    # 30 dakika bekle
    time.sleep(1800)
