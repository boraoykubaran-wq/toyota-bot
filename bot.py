import requests
from bs4 import BeautifulSoup
import time
import os

URL = "https://www.sahibinden.com/oto360/sifir-araclar/toyota-corolla-cross-fiyat-listesi"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_price():
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text(separator="\n")
    lines = text.split("\n")

    for i, line in enumerate(lines):
        if "Corolla Cross SUV" in line:
            # alt satırlarda fiyatı ara
            for j in range(i, i+5):
                if "TL" in lines[j]:
                    return lines[j].strip()

    return None
