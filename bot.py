def get_price():
    r = requests.get("https://www.toyota.com.tr/araba-modelleri/suv-araclar",
                     headers={"User-Agent": "Mozilla/5.0"})
    
    import re
    matches = re.findall(r"\d{1,3}(?:\.\d{3})+\s*TL", r.text)

    print("FOUND:", matches)

    if matches:
        return matches[0].replace(".", "").replace(" TL", "")

    return None
