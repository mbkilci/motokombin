import requests
from bs4 import BeautifulSoup
import re

def scrape_product_info(url):
    print(f"Scraping başlatılıyor (Truva Atı Proxy Modu): {url}")
    
    # Render IP'miz mimlendiği için araya vekil sunucular (Proxy) koyuyoruz.
    # Bu sistemler motoruma.com'a kendi IP'lerinden gidip HTML'i bize getirecek.
    proxy_urls = [
        f"https://api.allorigins.win/raw?url={url}",
        f"https://corsproxy.io/?{url}",
        url # Son çare doğrudan istek
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for proxy in proxy_urls:
        try:
            print(f"Deneniyor: {proxy[:40]}...")
            response = requests.get(proxy, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Cloudflare hala yakaladıysa diğer proxy'e geç
                page_text = soup.text.lower()
                if "just a moment" in page_text or "cloudflare" in page_text:
                    print("Cloudflare fark etti, diğer gizli yola geçiliyor...")
                    continue

                image_url = None
                price = "Bulunamadı"

                # 1. Meta Etiketi (En garantili)
                og_image = soup.find('meta', property='og:image')
                if og_image and og_image.get('content'):
                    image_url = og_image['content']
                    
                # 2. Resim Etiketleri
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
                    
        except Exception as e:
            print(f"Hata ({proxy[:30]}...): {e}")
            continue
            
    print("Tüm yollar denendi, görsel bulunamadı veya site erişimi tamamen kapalı.")
    return None