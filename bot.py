def get_price():
    import requests
    import re

    url = "https://www.toyota.com.tr/araba-modelleri/corolla-cross-hybrid"

    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    match = re.search(
        r"Başlangıç fiyatı\s*[:：]?\s*([\d\.]+)\s*TL",
        r.text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).replace(".", "")

    return None
