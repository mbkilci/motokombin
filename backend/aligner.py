from PIL import Image, ImageOps

ALIGNMENT_MAP = {
    "kask": {"x": 130, "y": 20, "w": 140, "h": 140},
    "mont": {"x": 80, "y": 140, "w": 240, "h": 260},
    # Pantolon biraz büyütüldü ve ortalandı
    "pantolon":  {"x": 110, "y": 370, "w": 160, "h": 310}, 
    "eldiven": {
        # Eldivenler biraz küçültüldü ve çok az sola kaydırıldı
        "left":  {"x": 20, "y": 345, "w": 80, "h": 95}, 
        "right": {"x": 270, "y": 345, "w": 80, "h": 95} 
    },
    "bot": {
        # Botlar belirgin şekilde büyütüldü ve dengelendi
        "left":  {"x": 105, "y": 615, "w": 95, "h": 115}, 
        "right": {"x": 200, "y": 615, "w": 95, "h": 115}  
    }
}

def align_and_composite(input_path, output_path, gear_type):
    try:
        gear_img = Image.open(input_path).convert("RGBA")
    except Exception as e:
        return False

    target = ALIGNMENT_MAP.get(gear_type)
    if not target:
        gear_img.save(output_path, "PNG")
        return True

    canvas = Image.new("RGBA", (400, 700), (0, 0, 0, 0))

    if gear_type in ["eldiven", "bot"]:
        # Ne gelirse gelsin, sola düz, sağa aynalı olarak bas
        left_img = gear_img
        right_img = ImageOps.mirror(gear_img)
        
        l_target = target["left"]
        left_img.thumbnail((l_target["w"], l_target["h"]), Image.Resampling.LANCZOS)
        l_x = l_target["x"] + (l_target["w"] - left_img.width) // 2
        l_y = l_target["y"] + (l_target["h"] - left_img.height) // 2
        canvas.paste(left_img, (l_x, l_y), left_img)
        
        r_target = target["right"]
        right_img.thumbnail((r_target["w"], r_target["h"]), Image.Resampling.LANCZOS)
        r_x = r_target["x"] + (r_target["w"] - right_img.width) // 2
        r_y = r_target["y"] + (r_target["h"] - right_img.height) // 2
        canvas.paste(right_img, (r_x, r_y), right_img)
        
    else:
        bbox = gear_img.getbbox()
        if bbox:
            gear_img = gear_img.crop(bbox)

        gear_img.thumbnail((target["w"], target["h"]), Image.Resampling.LANCZOS)
        paste_x = target["x"] + (target["w"] - gear_img.width) // 2
        paste_y = target["y"] + (target["h"] - gear_img.height) // 2
        canvas.paste(gear_img, (paste_x, paste_y), gear_img)

    canvas.save(output_path, "PNG")
    return True