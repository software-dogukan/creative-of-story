# models/vision_model.py

import os
import json
from ultralytics import YOLO
from datetime import datetime  # (Bu import'un yapıldığından emin olun)

# Kendi yardımcı dosyalarımızı import ediyoruz
from utils.config import MODELS_DIR, VISION_MODEL_NAME, VISION_CONFIDENCE_THRESHOLD
from utils.preprocess import save_analysis_json  # JSON kaydetme işini burada yapmak yerine utils'a taşıdık.

# Model yolunu config'den alıyoruz
VISION_MODEL_PATH = os.path.join(MODELS_DIR, VISION_MODEL_NAME)


class VisionAnalyzer:
    """
    YOLOv8 modelini kullanarak görüntüdeki nesneleri tespit eder.
    """

    def __init__(self, model_path=VISION_MODEL_PATH):
        # Modelin weights dosyasını yükler
        try:
            self.model = YOLO(model_path)
        except Exception as e:
            # Model dosyası yoksa indirmeyi deneyecek veya hata verecektir.
            print(f"YOLO modelini yüklerken hata oluştu: {e}")
            self.model = None

    def analyze(self, image_path):
        """
        Görüntü üzerinde nesne tespiti yapar.
        """
        if not self.model:
            # Hata durumunda, iki değer döndürerek app.py'deki unpacking hatasını önle.
            error_data = {"image_path": image_path, "detections": [],
                          "error": "Vision model yüklenemedi. 'yolov8n.pt' dosyasını kontrol edin."}
            return error_data, None

        detected_objects = []

        # YOLOv8'i çalıştırma. conf=VISION_CONFIDENCE_THRESHOLD ile filtreleme uyguluyoruz.
        # Stream=True, tek bir görsel için gereksiz ama genel kullanım için ideal.
        results = self.model.predict(
            source=image_path,
            conf=VISION_CONFIDENCE_THRESHOLD,
            verbose=False  # Çıktıyı temiz tutmak için
        )

        # İlk sonuç setini alıyoruz (tek bir görsel için tek sonuç setimiz var)
        if results:
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                confidence = float(box.conf[0])

                # `feature_extract.py` beklentisine uygun olarak formatlıyoruz
                detected_objects.append({
                    "label": label,  # 'object' yerine 'label' kullandık
                    "score": round(confidence, 4),
                    # İsteğe bağlı: Bounding Box koordinatlarını da ekleyebiliriz
                    # "box": box.xyxy[0].tolist()
                })

        # Tüm analiz verisini bir sözlükte toplama
        analysis_data = {
            "image_path": image_path,
            "detections": detected_objects,
            "timestamp": str(datetime.now())
        }

        # Analiz verisini utils/preprocess.py kullanarak JSON dosyasına kaydetme
        json_path = save_analysis_json(image_path, analysis_data)

        # <<< EKSİK OLAN SATIRLAR >>>
        # Ana uygulamanın kullanacağı veriyi döndürme
        return analysis_data, json_path
        # <<< EKSİK OLAN SATIRLAR SONU >>>