from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import requests

TOKEN = "SENIN_TOKEN"
CHAT_ID = "8421945805"

URL = "https://turkiye.toyota.com.tr/middle/fiyat-listesi/"

def send_message(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

def get_price():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(URL)
    time.sleep(5)

    body = driver.find_element(By.TAG_NAME, "body").text
    driver.quit()

    for line in body.split("\n"):
        if "Corolla Cross" in line and "TL" in line:
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
    new_price = get_price()
    old_price = load_old_price()

    print("Eski:", old_price)
    print("Yeni:", new_price)

    if new_price and new_price != old_price:
        send_message(f"🚗 Corolla Cross\n💰 Yeni fiyat: {new_price}")
        save_price(new_price)
    else:
        print("Değişiklik yok")

check_price()

while True:
    check_price()
    time.sleep(21600)  # 6 saat
