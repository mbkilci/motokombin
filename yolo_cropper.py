from ultralytics import YOLOWorld
from PIL import Image

print("YOLO-World modeli belleğe alınıyor...")
model = YOLOWorld('yolov8s-world.pt')

def crop_single_item_with_yolo(input_path, output_path, gear_type):
    if gear_type not in ["eldiven", "bot"]:
        img = Image.open(input_path)
        img.save(output_path)
        return True

    print(f"[{gear_type}] YOLO-World ile çift eşya taraması yapılıyor...")

    search_prompt = "shoe" if gear_type == "bot" else "glove"
    model.set_classes([search_prompt])
    
    results = model.predict(input_path, conf=0.05, verbose=False)
    img = Image.open(input_path)

    if len(results) > 0 and len(results[0].boxes) > 0:
        boxes = results[0].boxes.xyxy.cpu().numpy() 
        
        # --- İŞTE SENİN HARİKA ALGORİTMAN ---
        # Her bir kutunun Alanını (Genişlik x Yükseklik) hesapla ve EN BÜYÜĞÜNÜ seç.
        # Formul: (x2 - x1) * (y2 - y1)
        best_box = max(boxes, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
        
        x1, y1, x2, y2 = map(int, best_box)
        
        margin = 15
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = min(img.width, x2 + margin)
        y2 = min(img.height, y2 + margin)

        img = img.crop((x1, y1, x2, y2))
        print("🎯 YOLO başarılı! En BÜYÜK (öndeki) ürün sökülüp alındı.")
    else:
        print("⚠️ YOLO objeyi ayırt edemedi, orijinal görsel işleme giriyor.")

    img.save(output_path)
    return True