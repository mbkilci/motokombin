import requests
from bs4 import BeautifulSoup
import re

def scrape_product_info(url):
    print(f"İşlem başlatılıyor: {url}")
    
    # 0. YÖNTEM: DİREKT RESİM LİNKİ KONTROLÜ (Nihai Bypass)
    # Kullanıcı site linki yerine direkt resim adresini (sağ tık -> resim adresini kopyala) 
    # yapıştırdıysa, hiçbir korumaya takılmadan direkt resmi alırız!
    if url.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
        print("Direkt resim linki algılandı! Site engelleri tamamen atlanıyor.")
        return {"image_url": url, "price": "Fiyat Yok"}

    # 1. YÖNTEM: Microlink.io API (Çok güçlü ve engellenmesi zor bir okuyucu)
    try:
        print("Yöntem 1: Microlink API deneniyor...")
        res = requests.get(f"https://api.microlink.io?url={url}", timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data.get("data") and data["data"].get("image"):
                img_url = data["data"]["image"]["url"]
                print(f"Başarılı! Microlink Görseli: {img_url[:30]}...")
                return {"image_url": img_url, "price": "Bulunamadı"}
    except Exception as e:
        print(f"Microlink başarısız: {e}")

    # 2. YÖNTEM: Klasik Kazıma (Güvenliği düşük siteler için)
    try:
        print("Yöntem 2: Standart İstek deneniyor...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200 and "cloudflare" not in res.text.lower():
            soup = BeautifulSoup(res.content, 'html.parser')
            
            image_url = None
            price = "Bulunamadı"

            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                image_url = og_image['content']
            
            price_tag = soup.select_one('.product-price, .price, .current-price')
            if price_tag:
                price = re.sub(r'[^\d.,]', '', price_tag.text.strip())

            if image_url:
                print(f"Başarılı! Standart Görsel: {image_url[:30]}...")
                return {"image_url": image_url, "price": price}
    except Exception as e:
        print(f"Standart yöntem başarısız: {e}")

    print("Tüm yöntemler başarısız oldu. Lütfen ürün linki yerine DİREKT RESİM LİNKİ kullanın.")
    return None