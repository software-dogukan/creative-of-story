# app.py (NİHAİ VERSİYON - MULTI-MODAL AKIŞ)

import streamlit as st
import os

# Model Sınıfları
from models.vision_model import VisionAnalyzer
from models.story_model import StoryGenerator  # Artık bu, Gemini API'yi çağırıyor

# Yardımcı Fonksiyonlar ve Konfigürasyonlar
from utils.config import INPUT_IMAGES_DIR, PROCESSED_DIR, STORIES_DIR
from utils.preprocess import save_uploaded_image
from utils.story_utils import format_and_save_story, display_story_for_streamlit

# Gerekli dizinleri oluştur
for d in [INPUT_IMAGES_DIR, PROCESSED_DIR, STORIES_DIR]:
    os.makedirs(d, exist_ok=True)


def main():
    st.set_page_config(page_title="Akıllı Hikaye Üretici", layout="wide")
    st.title("🧠 Akıllı Hikaye Üretici (AI-Powered Story Generator)")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        uploaded_file = st.file_uploader(
            "Mağaza görseli yükleyin",
            type=["jpg", "png", "jpeg"],
            help="Yüklediğiniz görsel, nesne tespiti ve hikaye üretimi için kullanılacaktır."
        )

    if uploaded_file is not None:

        # 1.1. Görseli Kaydetme
        with st.spinner("Görsel sunucuya kaydediliyor..."):
            saved_img_path = save_uploaded_image(uploaded_file)
            original_file_name = uploaded_file.name

        if saved_img_path:
            with col2:
                st.image(saved_img_path, caption="Yüklenen Görsel", use_container_width=True)
            st.markdown("---")

            st.header("1. Hikaye Oluşturma 🚀")

            # --- KRİTİK DEĞİŞİM: YOLO ANALİZİ ARTIK STORY GENERATOR İÇİNDE ---
            if st.button("Hikaye Oluştur", key="start_analysis"):

                st.info("📖 Gemini ile görsel analiz edilip, hikaye oluşturuluyor...")

                # Hikaye Modeli Yükleme ve Üretim
                story_generator = StoryGenerator()

                with st.spinner("Görsel analizi yapılıyor ve metin üretiliyor..."):

                    # KRİTİK DEĞİŞİM: Sadece görsel yolunu gönderiyoruz.
                    # vision_analyzer ve analysis_data adımları atlandı!
                    raw_story_text = story_generator.generate(saved_img_path)

                st.markdown("---")
                st.header("2. Oluşturulan Hikaye")

                if raw_story_text and len(raw_story_text.strip()) > 10 and not raw_story_text.startswith(
                        ('Beklenmedik Hata', 'API Kısıtlama Hatası')):

                    # Hikayeyi Biçimlendir ve Kaydet
                    story_save_path = format_and_save_story(raw_story_text, original_file_name)
                    display_text = display_story_for_streamlit(raw_story_text)

                    st.success(f"Hikaye başarıyla üretildi ve kaydedildi: `{story_save_path}`")

                    st.subheader("Oluşturulan Mağaza Hikayesi")
                    st.markdown(f"> **{display_text}**")  # Kalın yapıldı

                else:
                    st.error(
                        "Hikaye oluşturulurken bir sorun oluştu veya model metin üretemedi. (Çıktı çok kısa veya boş)")

                    st.subheader("Oluşturulan Mağaza Hikayesi")

                    # Hata mesajını göster
                    st.markdown(f"> *{raw_story_text}*")

        else:
            st.error(
                "Görsel yüklenirken bir hata oluştu veya dosya kaydedilemedi. Lütfen dosya formatını kontrol edin.")


if __name__ == '__main__':
    main()