import cv2
import logging

import numpy as np

from src.models.factory import ModelFactory

class ImageService:
    def __init__(self, detector_name: str, recognizer_name: str) -> None:
        self.logger = logging.getLogger(__name__)
        self.model = ModelFactory.create_unified_model(detector_name, recognizer_name)
        self.logger.info(f"Loaded model: 人脸检测模型: {detector_name}, 情感识别模型: {recognizer_name}")
    
    def process(self, image: np.ndarray) -> list:
        result = []
        try:
            detection_result = self.model.detect_faces(image)
            for res in detection_result:
                x, y, w, h = res
                face_img = image[y:y+h, x:x+w]
                emotion_code = self.model.recognize_emotion(face_img)
                result.append((emotion_code, x, y, w, h))
        except Exception as e:
            self.logger.error(f"Processing error: {str(e)}")
            raise
        
        return result