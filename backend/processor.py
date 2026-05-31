from rembg import remove, new_session
from PIL import Image
import io
import os

# KRİTİK HIZLANDIRMA: Modeli sadece bir kere belleğe (Global Session) alıyoruz.
# Her Ekle butonuna basıldığında baştan yüklenmeyecek.
session = new_session("u2net")

def process_gear_image(input_path, output_path):
    print(f"[{input_path}] arka planı temizleniyor...")

    with open(input_path, 'rb') as i:
        input_data = i.read()

    # Session parametresini kullanarak süreyi saniyelere düşürüyoruz
    output_data = remove(input_data, session=session)
    
    img = Image.open(io.BytesIO(output_data))
    
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    img.save(output_path, 'PNG')
    print(f"Arka plan temizlendi: {output_path}")

if __name__ == "__main__":
    pass