# utils/config.py

import os

# --- TEMEL YOLLAR ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Veri Dizini Yolları
INPUT_IMAGES_DIR = os.path.join(DATA_DIR, "input_images")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
STORIES_DIR = os.path.join(DATA_DIR, "stories")

# Modeller Dizini Yolu
MODELS_DIR = os.path.join(BASE_DIR, "models")


# --- VİZYON MODELİ (YOLOv8) AYARLARI ---
VISION_MODEL_NAME = 'yolov8n.pt'
VISION_CONFIDENCE_THRESHOLD = 0.5  # Nesne algılama güven eşiği


# --- HİKAYE MODELİ (TRANSFORMERS) AYARLARI ---
# Yükleme hatasını ve kalitesiz çıktıyı çözmek için Türkçe GPT-2 modeli seçildi.
# Bu model, metin üretimi için tasarlanmıştır.
STORY_MODEL_NAME = 'ytu-ce-cosmos/turkish-gpt2-large' # Türkçe odaklı, daha büyük GPT-2

MAX_STORY_LENGTH = 1500 # Üretilecek maksimum kelime/token uzunluğu
TEMPERATURE = 0.6        # Yaratıcılık/rastgelelik seviyesi (0.0=Daha mantıklı, 1.0=Daha yaratıcı)


# --- JSON DOSYA AYARLARI ---
JSON_ANALYSIS_SUFFIX = "_analysis.json"