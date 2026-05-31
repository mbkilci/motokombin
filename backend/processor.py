# backend/processor.py

session = None

def process_gear_image(input_path, output_path):
    global session
    
    # 1. Kütüphaneyi en tepede değil, İÇERİDE çağırıyoruz. 
    # Bu sayede sunucu açılırken buralar hiç okunmaz, port anında açılır ve Render fişi çekmez.
    from rembg import remove, new_session
    
    # 2. Sadece 4 MB olan hafifletilmiş 'u2netp' modelini zorunlu kılıyoruz.
    if session is None:
        print("Hafif model (u2netp) ilk kez yukleniyor...")
        session = new_session("u2netp")
        
    # 3. Arka planı sil ve kaydet
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input_data = i.read()
            output_data = remove(input_data, session=session)
            o.write(output_data)