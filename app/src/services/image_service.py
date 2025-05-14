"""图像服务模块。

提供图像处理服务，包括人脸检测和表情识别功能。
"""

import logging

import numpy as np

from models.factory import ModelFactory

class ImageService:
    """图像服务类，用于处理图像中的人脸检测和表情识别。

    该类封装了人脸检测和表情识别的功能，提供统一的图像处理接口。
    """
    def __init__(self, detector_name: str, recognizer_name: str) -> None:
        self.logger = logging.getLogger(__name__)
        self.model = ModelFactory.create_unified_model(detector_name, recognizer_name)
        self.logger.info("Loaded model: 人脸检测模型: %s, 情感识别模型: %s", detector_name, recognizer_name)
    
    def process(self, image: np.ndarray) -> list:
        """处理图像，检测人脸并识别表情。

        Args:
            image: 输入图像数组

        Returns:
            list: 包含(表情代码, x1, y1, x2, y2)的列表，表示每个检测到的人脸位置和表情

        Raises:
            Exception: 处理过程中的任何错误
        """
        result = []
        try:
            detection_result = self.model.detect_faces(image)
            for res in detection_result:
                x1, y1, x2, y2 = res
                h = y2 - y1
                w = x2 - x1
                face_img = image[y1:y1+h, x1:x1+w]
                emotion_code = self.model.recognize_emotion(face_img)
                result.append((int(emotion_code), int(x1), int(y1), int(x2), int(y2)))
        except Exception as e:
            self.logger.error("Processing error: %s", str(e))
            raise
        
        return result 