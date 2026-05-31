from curl_cffi import requests
from bs4 import BeautifulSoup
import re

def scrape_product_info(url):
    print(f"Scraping başlatılıyor (Anti-Bot Chrome Modu): {url}")
    
    try:
        # impersonate="chrome110" komutu ile Cloudflare'i ağ paketi seviyesinde kandırıyoruz.
        # Site bu isteği gerçek bir Google Chrome'dan gelmiş gibi görecek.
        response = requests.get(url, impersonate="chrome110", timeout=15)
        
        if response.status_code != 200:
            print(f"Site hata döndürdü: {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        
        image_url = None
        price = "Bulunamadı"

        # 1. Meta Etiketi (En güveniliri)
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            image_url = og_image['content']
            
        # 2. Resim Etiketleri (Yedek Plan)
        if not image_url:
            img_tag = soup.select_one('.product-image img, #product-image, .main-image img')
            if img_tag and img_tag.get('src'):
                image_url = img_tag['src']

        # Fiyat Bulucu
        price_tag = soup.select_one('.product-price, .price, #product-price, span[itemprop="price"], .current-price')
        if price_tag:
             price = price_tag.text.strip()
             price = re.sub(r'[^\d.,]', '', price)

        if image_url:
            print(f"Başarılı! Görsel: {image_url[:30]}... Fiyat: {price}")
            return {"image_url": image_url, "price": price}
        else:
            print("Görsel HTML içinde bulunamadı.")
            return None
            
    except Exception as e:
        print(f"Bağlantı veya Kazıma Hatası: {e}")
        return None