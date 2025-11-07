# utils/preprocess.py

import os
from PIL import Image
import json
import uuid  # Dosya isimleri çakışmasın diye benzersiz ID oluşturmak için

# Kendi config dosyamızı import ediyoruz
from .config import INPUT_IMAGES_DIR, PROCESSED_DIR, JSON_ANALYSIS_SUFFIX


def save_uploaded_image(uploaded_file):
    """
    Streamlit'ten gelen yüklü dosyayı INPUT_IMAGES_DIR'a kaydeder.

    Args:
        uploaded_file: Streamlit file_uploader objesi (st.file_uploader)

    Returns:
        str: Kaydedilen dosyanın tam yolu.
    """
    if uploaded_file is None:
        return None

    # Benzersiz bir dosya adı oluşturma (çakışmaları önlemek için)
    # Orijinal uzantıyı koruma
    file_extension = os.path.splitext(uploaded_file.name)[1]
    unique_filename = str(uuid.uuid4()) + file_extension
    save_path = os.path.join(INPUT_IMAGES_DIR, unique_filename)

    # PIL Image ile dosyayı diske kaydetme
    try:
        image = Image.open(uploaded_file)
        # Görüntü formatını garanti altına almak ve büyük dosyaları küçültmek için (Opsiyonel)
        image.save(save_path)

        print(f"Görsel başarıyla kaydedildi: {save_path}")
        return save_path
    except Exception as e:
        print(f"Görsel kaydederken hata oluştu: {e}")
        return None


def save_analysis_json(image_path, analysis_data):
    """
    Görsel analiz sonuçlarını JSON formatında PROCESSED_DIR'a kaydeder.

    Args:
        image_path (str): Orijinal görselin tam yolu.
        analysis_data (dict): vision_model'den gelen analiz verisi.

    Returns:
        str: Kaydedilen JSON dosyasının tam yolu.
    """
    # Orijinal dosya adını al (uzantısız)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    json_filename = base_name + JSON_ANALYSIS_SUFFIX
    json_path = os.path.join(PROCESSED_DIR, json_filename)

    # JSON dosyasına kaydetme
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=4)

        print(f"Analiz JSON'u başarıyla kaydedildi: {json_path}")
        return json_path
    except Exception as e:
        print(f"JSON kaydederken hata oluştu: {e}")
        return None


def load_analysis_json(image_path):
    """
    Daha önce kaydedilmiş JSON analizini yükler.

    Args:
        image_path (str): Orijinal görselin tam yolu.

    Returns:
        dict or None: Yüklenen analiz verisi.
    """
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    json_filename = base_name + JSON_ANALYSIS_SUFFIX
    json_path = os.path.join(PROCESSED_DIR, json_filename)

    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"JSON okurken hata oluştu: {e}")
            return None
    return None