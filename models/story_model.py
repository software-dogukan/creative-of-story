# models/story_model.py (NİHAİ VE HATA AYIKLAMASI YAPILMIŞ VERSİYON)

import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError
from PIL import Image  # !!! GÖRSEL İŞLEME İÇİN !!!

# Kendi yardımcı dosyalarımız
from utils.config import MAX_STORY_LENGTH, TEMPERATURE

# .env dosyasındaki ortam değişkenlerini yükle
load_dotenv()


class StoryGenerator:

    def __init__(self):
        # KRİTİK DÜZELTME: self.client'ı her zaman tanımla (AttributeError'ı çözer)
        self.client = None
        self.model_name = "gemini-2.5-flash"

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            print("HATA: GEMINI_API_KEY ortam değişkeni bulunamadı. Lütfen .env dosyasını kontrol edin.")
            return

        try:
            # Gemini istemcisini anahtar ile başlat
            self.client = genai.Client(api_key=api_key)
            print(f"[StoryGenerator] Gemini API istemcisi başarıyla başlatıldı.")

        except Exception as e:
            print(f"Gemini istemcisi başlatılırken hata oluştu: {e}")
            # self.client, başlangıçta None olarak ayarlandığı için burada tekrar None'a ayarlamaya gerek yok.

    # !!! generate metodunun imzasını değiştiriyoruz !!!
    def generate(self, image_path, max_new_tokens=MAX_STORY_LENGTH, temperature=TEMPERATURE):

        if self.client is None:
            return "Hikaye modeli (Gemini API) başlatılamadı. API anahtarınızı ve internet bağlantınızı kontrol edin."

        try:
            # 1. Görseli yükle
            img = Image.open(image_path)

            # 2. Direkt komut metnini oluştur
            system_prompt = (
                "Sen yaratıcı bir mağaza tanıtım yazarıısın. Bu görseli analiz et ve "
                "içindeki ürünleri kullanarak müşteriyi çekecek, 4-5 cümlelik, akıcı ve duygusal bir reklam metni yaz. "
                "Cevabın sadece reklam hikayesinden oluşmalıdır. Reklam Metni: "
            )

            # 3. Metin ve görseli birlikte gönder (Multi-modal prompt)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[img, system_prompt],
                config={
                    "temperature": temperature,
                    "max_output_tokens": max_new_tokens,
                }
            )

            # 3.1. Yanıtın boş olup olmadığını kontrol et
            if response.text is None or not response.text.strip():
                if response.candidates:
                    finish_reason = response.candidates[0].finish_reason.name
                    if finish_reason == 'SAFETY':
                        return "API Kısıtlama Hatası: Üretim güvenlik filtrelerine takıldı. Lütfen görsel içeriğini kontrol edin."
                    elif finish_reason in ['MAX_TOKENS', 'STOPPED']:
                        return f"Beklenmedik Hata: Model, metin üretmeden durduruldu (Finish Reason: {finish_reason})."
                return "Beklenmedik Hata: API, metin döndüremedi. (Boş yanıt)."

            # 3.2. Başarılı Çıktı Temizliği
            story_text = response.text.strip()

            # Yeni sistemde prompt'u temizle
            if story_text.startswith("Reklam Metni:"):
                story_text = story_text[len("Reklam Metni:"):].strip()

            print("[StoryGenerator] Hikaye üretimi tamamlandı.")
            return story_text

        except APIError as e:
            return f"API Hatası: Hikaye üretilemedi. (Hata: {e})"
        except Exception as e:
            return f"Beklenmedik Hata: {e}"