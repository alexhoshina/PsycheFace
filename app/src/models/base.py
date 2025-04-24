from abc import ABC, abstractmethod
from typing import List, Dict

import numpy as np

class FaceDetectionModel(ABC):
    """人脸检测模型接口"""
    @abstractmethod
    def detect_faces(self, image: np.ndarray) -> List[Dict[str, int]]:
        """
        检测人脸，返回边界框列表
        格式：[{'x1': int, 'y1': int, 'x2': int, 'y2': int}, ...]
        """
        pass

class EmotionRecognitionModel(ABC):
    """表情识别模型接口"""
    @abstractmethod
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        预处理图像，返回适合模型输入的格式
        """
        pass
    
    @abstractmethod
    def recognize_emotion(self, face_image: np.ndarray) -> int:
        """
        识别表情，返回预定义表情代号（如 1=开心，2=悲伤等）
        """
        pass