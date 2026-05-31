import requests
import os
from scraper import scrape_product_info
from processor import process_gear_image

def download_image(url, save_path):
    print(f"Görsel indiriliyor: {url}")
    # User-Agent ekliyoruz ki siteler bizi bot sanıp engellemesin
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print("Görsel başarıyla diske kaydedildi.")
            return True
        else:
            print(f"Hata: Görsel indirilemedi. HTTP Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"İndirme sırasında bir hata oluştu: {e}")
        return False

def run_pipeline(product_url):
    print(f"\n=======================================")
    print(f"PİPELINE BAŞLATILDI: {product_url}")
    print(f"=======================================")
    
    # 1. Aşama: Veri Çekme (Scraping)
    data = scrape_product_info(product_url)
    img_url = data.get("image_url")
    price = data.get("price")
    
    if not img_url:
        print("Kritik Hata: Görsel URL'si bulunamadı, işlem iptal ediliyor.")
        return

    # 2. Aşama: Görseli İndirme
    # Pillow (PIL) kütüphanesi .webp, .jpg, .png gibi formatları otomatik tanır
    os.makedirs("temp_downloads", exist_ok=True)
    raw_image_path = "temp_downloads/temp_raw_image.webp" 
    
    success = download_image(img_url, raw_image_path)
    
    if success:
        # 3. Aşama: Görseli İşleme (Arka Plan Silme ve Kırpma)
        os.makedirs("final_outputs", exist_ok=True)
        final_image_path = "final_outputs/ready_to_use_gear.png"
        
        print("\nArka plan temizleme ve otomatik kırpma işlemine geçiliyor...")
        process_gear_image(raw_image_path, final_image_path)
        
        print("\n=======================================")
        print("🎯 İŞLEM BAŞARIYLA TAMAMLANDI!")
        print(f"💵 Çekilen Fiyat: {price}")
        print(f"🖼️ Hazır Görsel: {final_image_path} konumunda seni bekliyor.")
        print(f"=======================================\n")

if __name__ == "__main__":
    # Test için az önce kullandığın motoruma.com linkini kullanıyoruz
    test_url = "https://www.motoruma.com/hjc-rpha12-kapali-motosiklet-kaski-nardo-gri"
    run_pipeline(test_url)