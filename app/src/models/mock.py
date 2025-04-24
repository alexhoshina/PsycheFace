from typing import Dict, List
import numpy as np

from src.models.base import EmotionRecognitionModel, FaceDetectionModel
from src.models.factory import ModelFactory


@ModelFactory.register_detector("mock", model_path="null")
class MockDetector(FaceDetectionModel):
    """模拟人脸检测"""
    def __init__(self, model_path: str):
        pass
    def detect_faces(self, image: np.ndarray) -> List[Dict[str, int]]:
        return [{'x1': 100, 'y1': 100, 'x2': 200, 'y2': 200}]

@ModelFactory.register_recognizer("mock", model_path="null")
class MockRecognizer(EmotionRecognitionModel):
    """模拟表情识别"""
    def __init__(self, model_path: str):
        pass
    def recognize_emotion(self, face_image: np.ndarray) -> int:
        return int(1)