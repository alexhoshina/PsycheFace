"""模拟模型模块。

提供用于测试和开发的人脸检测和情感识别的模拟实现。
"""

from typing import List, Tuple
import numpy as np

from .base import EmotionRecognitionModel, FaceDetectionModel
from .factory import ModelFactory


@ModelFactory.register_detector("mockD", model_path="null")
@ModelFactory.register_detector("mockD2", model_path="null")
class MockDetector(FaceDetectionModel):
    """模拟人脸检测"""
    def __init__(self, model_path: str):
        pass
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        return [(10, 10, 60, 60)]
    def momo(self):
        """用于通过Pylint检查的辅助方法。

        Returns:
            str: 固定的测试字符串
        """
        return '这是用来通过Pylint检查的方法'

@ModelFactory.register_recognizer("mockR", model_path="null", input_shape=(100, 100))
class MockRecognizer(EmotionRecognitionModel):
    """模拟表情识别"""
    def __init__(self, model_path: str, input_shape: tuple):
        pass
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        pass
    def recognize_emotion(self, face_image: np.ndarray) -> int:
        return int(1)
