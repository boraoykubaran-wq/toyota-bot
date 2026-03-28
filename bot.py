import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 🔑 SENİN BİLGİLERİN
TOKEN = "8768272603:AAFTYPyzQQGnCGR1CRMGw58tEN_nQc-9FSE"
CHAT_ID = "8421945805"
URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/"

# 📩 TELEGRAM MESAJ
def send_message(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Mesaj gönderme hatası:", e)

# 💾 ESKİ FİYATI YÜKLE
def load_old_price():
    if os.path.exists("price.txt"):
        with open("price.txt", "r") as f:
            return f.read().strip()
    return None

# 💾 FİYATI KAYDET
def save_price(price):
    with open("price.txt", "w") as f:
        f.write(price)

# 🌐 FİYATI ÇEK
def get_price():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(URL)
        time.sleep(5)

        # Çerez kabul
        try:
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Tümüne izin ver')]")))
            btn.click()
        except:
            pass

        # Corolla Cross linkini bul
        links = driver.find_elements(By.TAG_NAME, "a")
        target_link = next(
            (l.get_attribute("href") for l in links
             if l.get_attribute("href") and "corolla-cross" in l.get_attribute("href").lower()),
            None
        )

        if not target_link:
            return None

        driver.get(target_link)
        time.sleep(7)

        body_text = driver.find_element(By.TAG_NAME, "body").text

        for line in body_text.split("\n"):
            if "Flame" in line and "TL" in line:
                return line.strip()

        return None

    except Exception as e:
        print("Fiyat çekme hatası:", e)
        return None

    finally:
        driver.quit()

# 🔁 ANA DÖNGÜ

old_price = load_old_price()

# İlk çalışmada bilgi mesajı
send_message("🤖 Bot aktif! Fiyat takibi başladı...")

while True:
    print("Fiyat kontrol ediliyor...")

    new_price = get_price()

    if new_price:
        print("Bulunan fiyat:", new_price)

    if new_price and new_price != old_price:
        send_message(
            f"🚗 Corolla Cross Fiyat Güncellendi!\n\n"
            f"💰 {new_price}"
        )
        save_price(new_price)
        old_price = new_price

    time.sleep(1800)  # 30 dakika
