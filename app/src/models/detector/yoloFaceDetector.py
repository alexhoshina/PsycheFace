import numpy as np
from ultralytics import YOLO
from typing import List, Dict, Tuple

from src.models.base import FaceDetectionModel
from src.models.factory import ModelFactory

@ModelFactory.register_detector("yolo_v5", model_path="yolov5.pt")
class YoloFaceDetector(FaceDetectionModel):
    """YOLO人脸检测实现"""
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        results = self.model(image)
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int).tolist()
        return [(int(box[0]),int(box[1]),int(box[2]),int(box[3])) for box in boxes]