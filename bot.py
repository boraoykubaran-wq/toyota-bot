from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

# 🔑 SENİN TOKEN
TOKEN = "8768272603:AAFTYPyzQQGnCGR1CRMGw58tEN_nQc-9FSE"
CHAT_ID = "8421945805"

URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/"

def send_message(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

def get_price():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    driver.get(URL)

    # 🍪 COOKIE
    try:
        btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Tümüne izin ver')]")
        ))
        btn.click()
    except:
        pass

    time.sleep(3)

    # 🚗 COROLLA CROSS LINK BUL
    links = driver.find_elements(By.TAG_NAME, "a")

    target_link = None
    for link in links:
        href = link.get_attribute("href")
        if href and "corolla-cross" in href.lower():
            target_link = href
            break

    if not target_link:
        driver.quit()
        return None

    driver.get(target_link)
    time.sleep(5)

    body = driver.find_element(By.TAG_NAME, "body").text
    driver.quit()

    # 💰 FİYAT BUL
    for line in body.split("\n"):
        if "₺" in line or "TL" in line:
            return line

    return None

def load_old_price():
    try:
        with open("price.txt", "r") as f:
            return f.read()
    except:
        return None

def save_price(price):
    with open("price.txt", "w") as f:
        f.write(price)

def check_price():
    try:
        new_price = get_price()
        old_price = load_old_price()

        print("Eski:", old_price)
        print("Yeni:", new_price)

        if new_price and new_price != old_price:
            send_message(f"🚗 Corolla Cross\n💰 Yeni fiyat: {new_price}")
            save_price(new_price)
        else:
            print("Değişiklik yok")

    except Exception as e:
        print("HATA:", e)

# 🔁 LOOP
while True:
    check_price()
    time.sleep(3600)