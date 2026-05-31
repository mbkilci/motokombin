import cloudscraper
from bs4 import BeautifulSoup
import re

def scrape_product_info(url):
    print(f"Scraping başlatılıyor (Hayalet Mod): {url}")
    
    # cloudscraper, standart requests'in gelişmiş, bot korumalarını aşabilen halidir
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    try:
        response = scraper.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        image_url = None
        price = "Bulunamadı"

        # Görseli Bulma (Sitenin yapısına göre genel bir arama)
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            image_url = og_image['content']
            
        if not image_url:
            img_tag = soup.select_one('.product-image img, #product-image, .main-image img')
            if img_tag and img_tag.get('src'):
                image_url = img_tag['src']

        # Fiyatı Bulma
        price_tag = soup.select_one('.product-price, .price, #product-price, span[itemprop="price"]')
        if price_tag:
             price = price_tag.text.strip()
             price = re.sub(r'[^\d.,]', '', price)

        if not image_url:
             print("Hata: Görsel bulunamadı.")
             return None

        print(f"Başarılı! Görsel: {image_url[:30]}... Fiyat: {price}")
        return {"image_url": image_url, "price": price}

    except Exception as e:
        print(f"Scraping Hatası (Cloudflare Engeli Olabilir): {e}")
        return None