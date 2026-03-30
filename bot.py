from playwright.sync_api import sync_playwright

def get_price():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.toyota.com.tr/araba-modelleri/suv-araclar")

            content = page.content()

            import re
            matches = re.findall(r"\d{1,3}(?:\.\d{3})+\s*TL", content)

            browser.close()

            if matches:
                return matches[0].replace(".", "").replace(" TL", "")

    except Exception as e:
        print("HATA:", e)

    return None
