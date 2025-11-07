# app.py (GELİŞTİRİLMİŞ ARAYÜZ VERSİYONU)

import streamlit as st
import os

# Model Sınıfları
# Artık sadece StoryGenerator'a odaklanıyoruz
from models.story_model import StoryGenerator

# Yardımcı Fonksiyonlar ve Konfigürasyonlar
from utils.config import INPUT_IMAGES_DIR, PROCESSED_DIR, STORIES_DIR
from utils.preprocess import save_uploaded_image
from utils.story_utils import format_and_save_story, display_story_for_streamlit

# Gerekli dizinleri oluştur
for d in [INPUT_IMAGES_DIR, PROCESSED_DIR, STORIES_DIR]:
    os.makedirs(d, exist_ok=True)


def main():
    # --- 1. Sayfa Ayarları ve CSS İyileştirmeleri ---
    st.set_page_config(
        page_title="Akıllı Hikaye Üretici",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Basit CSS ile başlık ve arka plan iyileştirmesi
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5em;
            font-weight: bold;
            color: #3B71CA; /* Mavi tonu */
            text-align: center;
            margin-bottom: 0.5em;
        }
        .stButton>button {
            background-color: #3B71CA;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stAlert {
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="main-header">🧠 Akıllı Mağaza Hikayesi Üreticisi</p>', unsafe_allow_html=True)
    st.markdown("---")

    # --- 2. Yükleme ve Önizleme Alanları ---
    col_upload, col_preview = st.columns([1, 2])

    with col_upload:
        st.subheader("1. Görsel Yükle")
        uploaded_file = st.file_uploader(
            "Mağaza içi bir fotoğraf seçin",
            type=["jpg", "png", "jpeg"],
            accept_multiple_files=False,
            help="Yapay zeka, bu görseli analiz ederek bir reklam hikayesi oluşturacaktır."
        )

    if uploaded_file is not None:

        # 1.1. Görseli Kaydetme
        with st.spinner("Görsel sunucuya kaydediliyor..."):
            saved_img_path = save_uploaded_image(uploaded_file)
            original_file_name = uploaded_file.name

        if saved_img_path:
            with col_preview:
                st.subheader("2. Görsel Önizleme")
                st.image(saved_img_path, caption="Analiz Edilecek Görsel", use_container_width=True)

            st.markdown("---")

            # --- 3. İşlem Butonu ve Akış ---

            st.subheader("3. Yapay Zeka Analizini Başlat")

            # Başlat butonu
            if st.button("Hikaye Oluştur ve Kaydet", key="start_analysis"):

                # Modelin sadece bir kez yüklenmesi için state kullanmak performansı artırır (Opsiyonel)
                if 'story_generator' not in st.session_state:
                    st.session_state.story_generator = StoryGenerator()

                story_generator = st.session_state.story_generator

                st.info("📖 Gemini ile görsel analiz edilip, yaratıcı reklam metni oluşturuluyor...")

                with st.spinner("Görsel analiz ediliyor ve metin üretiliyor... Bu işlem 5-10 saniye sürebilir."):
                    raw_story_text = story_generator.generate(saved_img_path)

                st.markdown("---")

                # --- 4. Sonuçların Gösterimi ---

                st.header("✨ Oluşturulan Mağaza Hikayesi")

                # Başarılı durum
                if raw_story_text and len(raw_story_text.strip()) > 10 and not raw_story_text.startswith(
                        ('Beklenmedik Hata', 'API Kısıtlama Hatası')):

                    story_save_path = format_and_save_story(raw_story_text, original_file_name)
                    display_text = display_story_for_streamlit(raw_story_text)

                    st.success(f"Hikaye başarıyla üretildi ve kaydedildi: {story_save_path.split('data')[1]}")

                    # BAŞARILI METİN GÖSTERİMİ DÜZELTİLDİ: Metin rengi koyu gri, arka plan açık mavi
                    st.markdown(
                        f'<div style="background-color: #e0f7fa; padding: 20px; border-radius: 8px; border-left: 5px solid #007bb5;">'  # Açık mavi arka plan, koyu mavi çerçeve
                        f'<p style="font-size: 1.2em; line-height: 1.6; color: #333333;">{display_text}</p>'  # Koyu gri metin rengi
                        f'</div>', unsafe_allow_html=True)
                else:
                    # Hata durumu
                    st.error("Hikaye oluşturulurken bir sorun oluştu veya model metin üretemedi.")

                    st.subheader("Oluşturulan Mağaza Hikayesi")

                    # HATA METNİ GÖSTERİMİ DÜZELTİLDİ: Metin rengi kırmızı, arka plan açık kırmızı
                    st.markdown(
                        f'<div style="background-color: #ffe0e0; padding: 10px; border: 1px solid #cc0000; border-radius: 5px;">'  # Açık kırmızı arka plan, koyu kırmızı çerçeve
                        f'<p style="color: #cc0000; font-weight: bold;">{raw_story_text}</p>'  # Koyu kırmızı metin rengi
                        f'</div>', unsafe_allow_html=True)

            else:
                st.error("Görsel yüklenirken bir hata oluştu veya dosya kaydedilemedi.")

if __name__ == '__main__':
    main()