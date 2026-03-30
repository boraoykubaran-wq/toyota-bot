def get_price():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")

        import re

        # Tüm TL fiyatlarını bul
        matches = re.findall(r"(\d{1,3}(?:\.\d{3})+)\s*TL", soup.get_text())

        if matches:
            # genelde ilk fiyat başlangıç fiyatıdır
            price = matches[0]
            return price.replace(".", "")

    except Exception as e:
        print("HATA:", e)

    return None
