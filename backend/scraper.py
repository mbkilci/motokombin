import requests
from bs4 import BeautifulSoup
import re

def scrape_product_info(url):
    print(f"Scraping başlatılıyor (3 Katmanlı Bypass Modu): {url}")
    
    # 1. YÖNTEM: Googlebot (SEO kılığı - Siteler Google'ı engellemekten korkar)
    try:
        print("Yöntem 1: Googlebot Kılığı deneniyor...")
        headers = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200 and "cloudflare" not in res.text.lower() and "just a moment" not in res.text.lower():
            soup = BeautifulSoup(res.content, 'html.parser')
            result = parse_html(soup)
            if result:
                return result
    except Exception as e:
        print(f"Yöntem 1 Başarısız: {e}")

    # 2. YÖNTEM: Dub.co Metatags API (Çok Güçlü, Güvenilir Sistem)
    try:
        print("Yöntem 2: Özel Metatag API deneniyor...")
        api_url = f"https://api.dub.co/metatags?url={url}"
        res = requests.get(api_url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data.get("image"):
                print(f"Başarılı! API'den Görsel bulundu: {data['image'][:30]}...")
                # Bu API fiyat döndürmez ama görseli 100% garanti getirir.
                return {"image_url": data["image"], "price": "Bulunamadı"}
    except Exception as e:
        print(f"Yöntem 2 Başarısız: {e}")

    # 3. YÖNTEM: AllOrigins JSON API (Timeout sorununu aşan JSON sürümü)
    try:
        print("Yöntem 3: AllOrigins JSON deneniyor...")
        res = requests.get(f"https://api.allorigins.win/get?url={url}", timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data.get("contents") and "cloudflare" not in data.get("contents").lower():
                soup = BeautifulSoup(data["contents"], 'html.parser')
                result = parse_html(soup)
                if result:
                    return result
    except Exception as e:
        print(f"Yöntem 3 Başarısız: {e}")

    print("Tüm bypass yöntemleri başarısız oldu. Site bir kale gibi korunuyor.")
    return None

def parse_html(soup):
    image_url = None
    price = "Bulunamadı"

    og_image = soup.find('meta', property='og:image')
    if og_image and og_image.get('content'):
        image_url = og_image['content']
        
    if not image_url:
        img_tag = soup.select_one('.product-image img, #product-image, .main-image img')
        if img_tag and img_tag.get('src'):
            image_url = img_tag['src']

    price_tag = soup.select_one('.product-price, .price, #product-price, span[itemprop="price"], .current-price')
    if price_tag:
         price_text = price_tag.text.strip()
         price = re.sub(r'[^\d.,]', '', price_text)

    if image_url:
        print(f"Başarılı! Görsel ayrıştırıldı: {image_url[:30]}... Fiyat: {price}")
        return {"image_url": image_url, "price": price}
    return None