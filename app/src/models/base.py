"""基础模型接口定义模块。

该模块定义了人脸检测和情感识别的基础抽象类接口。
"""

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
    @abstractmethod
    def get_info(self) -> dict:
        """获取模型信息。

        Returns:
            dict: 包含模型名称、版本等信息的字典
        """

class EmotionRecognitionModel(ABC):
    """表情识别模型接口"""
    @abstractmethod
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        预处理图像，返回适合模型输入的格式
        """
    @abstractmethod
    def recognize_emotion(self, face_image: np.ndarray) -> int:
        """
        识别表情，返回预定义表情代号（如 1=开心，2=悲伤等）
        """
        