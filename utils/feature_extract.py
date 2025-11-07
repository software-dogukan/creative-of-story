# utils/feature_extract.py (GÜNCELLENMİŞ VERSİYON)

# (Diğer importlar...)
# from .config import ... # Gerekirse

def _extract_objects_from_analysis(analysis_data):
    """
    vision_model'den gelen analiz verisinden temiz nesne etiketlerini çıkarır.

    Args:
        analysis_data (dict): vision_model'den gelen ham analiz verisi.

    Returns:
        list: Temizlenmiş nesne etiketlerinin listesi.
    """

    # Yeni vision_model'imizde anahtar 'detections' ve alt anahtar 'label'
    detections = analysis_data.get('detections', [])
    objects = []

    # Farklı anahtar isimlerini destekleyen güçlü bir çekme mantığı
    for o in detections:
        # 'label' veya 'object' anahtarlarını arar
        label = o.get("label") or o.get("object") or None

        if label:
            # Temizleme: Eğer etiketler yol veya özel karakter içeriyorsa temizle
            label = str(label).replace("\\", " ").replace("/", " ").strip()
            # Tekrarlayan kelimeleri (örneğin iki 'person' tespit edildiyse) tekil hale getirmek için
            # burayı daha sonra iyileştirebiliriz, şimdilik sadece etiketleri topluyoruz.
            objects.append(label)

    # Sadece benzersiz (unique) nesneleri kullanmak daha iyi bir prompt sağlar:
    return list(set(objects))


def create_story_prompt(analysis_data, language="tr"):
    unique_items = _extract_objects_from_analysis(analysis_data)

    # KRİTİK DEĞİŞİM: Sadece ilk 5 benzersiz öğeyi kullan
    selected_items = unique_items[:5]

    if not selected_items:
        return "Resimde herhangi bir ürün tespit edilemedi. Lütfen yaratıcı ve kısa bir mağaza reklamı metni oluşturun.\n\nHikaye Metni: "

    item_list_str = ", ".join(selected_items)

    # Prompt metnini minimuma indiriyoruz
    if language == "tr":
        prompt = (
            "oluşturacağın hikaye 100 kelimeden oluştur Aşağıdaki 5 ana ürünü içeren, 4 cümlelik, ilgi çekici bir mağaza reklam metni oluştur: "
            f"Ürünler: {item_list_str}\n\n"
            "Reklam Metni: "
        )
    else:
        prompt = (
            f"Write a 4-sentence, compelling store marketing copy featuring these 5 main products: {item_list_str}\n\nStory: "
        )

    return prompt