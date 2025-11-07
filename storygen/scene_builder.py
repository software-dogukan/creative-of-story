import json
import os

def build_scene_description(json_path):
    # 1️⃣ JSON dosyasını oku
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2️⃣ Nesneleri liste olarak al
    objects = [obj["object"] for obj in data["objects"]]

    # 3️⃣ Eğer nesne bulunamadıysa, varsayılan mesaj döndür
    if not objects:
        return "No objects detected in the image."

    # 4️⃣ Nesneleri bağlayıcı bir cümle haline getir
    if len(objects) == 1:
        scene_description = f"The image contains a {objects[0]}."
    elif len(objects) == 2:
        scene_description = f"The image contains a {objects[0]} and a {objects[1]}."
    else:
        scene_description = f"The image shows a {', '.join(objects[:-1])}, and a {objects[-1]}."

    # 5️⃣ Opsiyonel olarak sahneye duygu veya ortam ekle
    scene_description += " The atmosphere seems calm and natural."

    return scene_description


if __name__ == "__main__":
    # Test için dosya yolu
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(BASE_DIR, "data", "processed", "test_features.json")

    description = build_scene_description(json_path)
    print("📝 Scene Description:")
    print(description)
