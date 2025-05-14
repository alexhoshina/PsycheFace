"""YOLO人脸检测模型模块。

使用YOLOv5模型进行人脸检测。
"""

from typing import List, Tuple

import numpy as np
from ultralytics import YOLO

from ..base import FaceDetectionModel
from ..factory import ModelFactory

@ModelFactory.register_detector("yolo_v5", model_path="yolov5.pt")
class YoloFaceDetector(FaceDetectionModel):
    """YOLO人脸检测实现"""
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """使用YOLO模型检测图像中的人脸。

        Args:
            image: 输入图像数组

        Returns:
            List[Tuple[int, int, int, int]]: 人脸边界框列表，每个边界框为 (x1, y1, x2, y2)
        """
        results = self.model(image)
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int).tolist()
        return [(int(box[0]),int(box[1]),int(box[2]),int(box[3])) for box in boxes]
