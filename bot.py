def get_price():
    try:
        import requests
        import re

        url = "https://www.toyota.com.tr/araba-modelleri/corolla-cross-hybrid"

        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        # SADECE başlangıç fiyatını hedefliyoruz
        match = re.search(r"Başlangıç fiyatı\s*[:：]?\s*([\d\.]+)\s*TL", r.text)

        if match:
            price = match.group(1)
            print("FOUND PRICE:", price)
            return price.replace(".", "")

    except Exception as e:
        print("HATA:", e)

    return None
