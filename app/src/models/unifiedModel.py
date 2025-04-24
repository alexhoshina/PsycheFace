from typing import Dict, List, Tuple
import numpy as np
from src.models.base import EmotionRecognitionModel, FaceDetectionModel


class UnifiedModel:
    """对外暴露的统一模型接口"""
    def __init__(self, detector: FaceDetectionModel, recognizer: EmotionRecognitionModel):
        self._detector = detector
        self._recognizer = recognizer
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        return self._detector.detect_faces(image)
    
    def recognize_emotion(self, face_image: np.ndarray) -> int:
        return self._recognizer.recognize_emotion(face_image)