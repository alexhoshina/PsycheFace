"""统一模型模块。

提供将人脸检测和情感识别模型组合的统一接口。
"""

from typing import List, Tuple
import numpy as np
from .base import EmotionRecognitionModel, FaceDetectionModel


class UnifiedModel:
    """对外暴露的统一模型接口"""
    def __init__(self, detector: FaceDetectionModel, recognizer: EmotionRecognitionModel):
        self._detector = detector
        self._recognizer = recognizer
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """检测图像中的人脸。

        Args:
            image: 输入图像数组

        Returns:
            List[Tuple[int, int, int, int]]: 人脸边界框列表，每个边界框为 (x1, y1, x2, y2)
        """
        return self._detector.detect_faces(image)
    def recognize_emotion(self, face_image: np.ndarray) -> int:
        """识别人脸图像中的表情。

        Args:
            face_image: 人脸图像数组

        Returns:
            int: 表情代号（如 1=开心，2=悲伤等）
        """
        return self._recognizer.recognize_emotion(face_image)
