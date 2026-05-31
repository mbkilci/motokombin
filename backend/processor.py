from rembg import remove, new_session
import os

# Session'ı en başta BOŞ bırakıyoruz ki sunucu açılırken indirme yapıp kilitlenmesin.
session = None

def get_session():
    global session
    if session is None:
        print("Yapay zeka modeli ilk kez yükleniyor (u2netp)...")
        # İlk görsel isteği geldiğinde sadece 4MB olan hafifletilmiş modeli indirir ve hafızada tutar.
        session = new_session("u2netp")
    return session

def process_gear_image(input_path, output_path):
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input_data = i.read()
            # Arka plan silme işlemine bu tembel session'ı gönderiyoruz
            output_data = remove(input_data, session=get_session())
            o.write(output_data)