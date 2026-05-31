from rembg import remove, new_session
import os

# Render'ın 512MB RAM sınırına takılmamak için sadece 4MB olan hafifletilmiş 'u2netp' modelini tanımlıyoruz.
# İlk çalışmada bir kere indirir ve önbelleğe alır.
session = new_session("u2netp")

def process_gear_image(input_path, output_path):
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input_data = i.read()
            # Arka plan silme işlemine bu hafif session'ı gönderiyoruz
            output_data = remove(input_data, session=session)
            o.write(output_data)