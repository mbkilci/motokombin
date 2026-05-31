import requests
from bs4 import BeautifulSoup
import re

def scrape_product_info(url):
    print(f"Scraping başlatılıyor (Hızlı Mod): {url}")
    
    # Gerçek bir tarayıcı gibi davranarak sitenin engellemesini önlüyoruz
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        image_url = None
        price = "Bulunamadı"

        # Görseli Bulma (Sitenin yapısına göre genel bir arama)
        # 1. Yöntem: Meta etiketleri (En güveniliri)
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            image_url = og_image['content']
            
        # 2. Yöntem: Sitedeki büyük ürün görselleri (Eğer og:image yoksa)
        if not image_url:
            img_tag = soup.select_one('.product-image img, #product-image, .main-image img')
            if img_tag and img_tag.get('src'):
                image_url = img_tag['src']

        # Fiyatı Bulma
        price_tag = soup.select_one('.product-price, .price, #product-price, span[itemprop="price"]')
        if price_tag:
             price = price_tag.text.strip()
             # Fiyatı temizle (Sadece rakamları ve virgülü/noktayı bırak)
             price = re.sub(r'[^\d.,]', '', price)

        if not image_url:
             print("Hata: Görsel bulunamadı.")
             return None

        print(f"Başarılı! Görsel: {image_url[:30]}... Fiyat: {price}")
        return {"image_url": image_url, "price": price}

    except Exception as e:
        print(f"Scraping Hatası: {e}")
        return None