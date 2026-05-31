import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def scrape_fast(url):
    """Hızlı HTTP isteği ile veriyi çeker (0.2-0.5 sn)"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Sitenin kapak fotoğrafını (Kusursuz kalite) çeker
        img_tag = soup.find("meta", property="og:image")
        if not img_tag:
            return None
        image_url = img_tag.get("content")
        
        # Fiyatı bul
        price = "Bulunamadı"
        price_tag = soup.find("meta", property="product:price:amount")
        if price_tag:
            price = price_tag.get("content")
        else:
            common_selectors = [".product-price", ".price-value", "span[itemprop='price']", ".current-price"]
            for sel in common_selectors:
                elem = soup.select_one(sel)
                if elem and elem.text.strip():
                    price = elem.text.strip()
                    break
                    
        return {"image_url": image_url, "price": price}
    except Exception as e:
        print(f"Hızlı çekim hatası: {e}")
        return None

def scrape_with_selenium(url):
    """Selenium yedeği - Işık hızı başarısız olursa çalışır."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(1.5) # Bekleme süresi minimal
    
    result = {"image_url": None, "price": None}
    
    try:
        img_element = driver.find_element(By.XPATH, "//meta[@property='og:image']")
        result["image_url"] = img_element.get_attribute("content")
        
        try:
            price_element = driver.find_element(By.XPATH, "//meta[@property='product:price:amount']")
            result["price"] = price_element.get_attribute("content")
        except:
            pass
                    
    except Exception as e:
        print("Selenium görseli bulamadı.", e)
        
    driver.quit()
    return result

def scrape_product_info(url, _=None): # gear_type parametresini artık kullanmıyoruz
    # Eğer direkt görsel linkiyse DOM tarama, direkt al
    clean_url = url.lower().split('?')[0]
    if clean_url.endswith(('.png', '.jpg', '.jpeg', '.webp')):
        print("📸 Direkt görsel linki algılandı! Işık hızında işlem yapılıyor.")
        return {"image_url": url, "price": "0 TL"}
    
    print(f"\n[{url}] adresine gidiliyor...")
    
    fast_data = scrape_fast(url)
    if fast_data and fast_data.get("image_url"):
        print("⚡ Veri BeautifulSoup ile ışık hızında çekildi!")
        return fast_data
        
    print("⏳ JS render gerekli, Selenium başlatılıyor...")
    return scrape_with_selenium(url)