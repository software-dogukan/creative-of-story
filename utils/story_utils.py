# utils/story_utils.py

import os
import datetime
from .config import STORIES_DIR


def format_and_save_story(story_text, original_image_name):
    """
    Üretilen hikaye metnini biçimlendirir ve stories dizinine kaydeder.

    Args:
        story_text (str): Dil modeli tarafından üretilen ham hikaye metni.
        original_image_name (str): Hikayenin oluşturulduğu orijinal görselin adı (uzantılı).

    Returns:
        str: Kaydedilen dosyanın tam yolu.
    """
    # 1. Başlık ve Zaman Damgası Oluşturma

    # Görsel adına dayalı basit bir başlık
    image_base_name = os.path.splitext(original_image_name)[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    story_title = f"Hikaye Analizi: {image_base_name}"

    # 2. Kaydedilecek Metni Biçimlendirme

    # Kaydedilecek metnin başına meta veri ekleme
    full_story_content = (
        f"--- {story_title} ---\n"
        f"Oluşturulma Tarihi: {timestamp}\n"
        f"Analiz Edilen Görsel: {original_image_name}\n\n"
        f"--- HİKAYE METNİ ---\n"
        f"{story_text.strip()}\n"
        f"---------------------\n"
    )

    # 3. Dosya Adı ve Kayıt Yolu

    # Kayıt dosya adı: timestamp_orijinalad.txt
    file_name = f"{timestamp}_{image_base_name}.txt"
    save_path = os.path.join(STORIES_DIR, file_name)

    # 4. Kayıt İşlemi
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(full_story_content)

        print(f"Hikaye başarıyla kaydedildi: {save_path}")
        return save_path
    except Exception as e:
        print(f"Hikaye kaydederken hata oluştu: {e}")
        return None


def display_story_for_streamlit(story_text):
    """
    Üretilen hikaye metnini Streamlit'te gösterim için hazırlar (basit temizlik).

    Args:
        story_text (str): Ham hikaye metni.

    Returns:
        str: Görüntülenmeye hazır temizlenmiş metin.
    """
    # Ekstra boşlukları ve modelin tekrarlayıcı kısımlarını temizleyebiliriz
    cleaned_text = story_text.strip()

    # GPT-2 bazen prompt'u tekrar eder, bunu kesmek için basit bir kontrol
    # Ancak bu, dil modelinin çıktısına göre hassas ayar gerektirir.

    return cleaned_text