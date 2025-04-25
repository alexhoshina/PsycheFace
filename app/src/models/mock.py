from typing import Dict, List, Tuple
import numpy as np

from src.models.base import EmotionRecognitionModel, FaceDetectionModel
from src.models.factory import ModelFactory


@ModelFactory.register_detector("mockD", model_path="null")
@ModelFactory.register_detector("mockD2", model_path="null")
class MockDetector(FaceDetectionModel):
    """模拟人脸检测"""
    def __init__(self, model_path: str):
        pass
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        return [(0, 0, 0, 0)]

@ModelFactory.register_recognizer("mockR", model_path="null", input_shape=(100, 100))
class MockRecognizer(EmotionRecognitionModel):
    """模拟表情识别"""
    def __init__(self, model_path: str, input_shape: tuple):
        print(input_shape)
        pass
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        pass
    def recognize_emotion(self, face_image: np.ndarray) -> int:
        return int(1)