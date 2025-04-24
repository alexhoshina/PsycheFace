import logging
from PIL import Image
import numpy as np
from io import BytesIO
from src.models.factory import ModelFactory

class ImageProcessor:
    """
    图像处理服务
    负责模型推理和结果整合
    """
    def __init__(self, detector_name: str, recognizer_name: str) -> None:
        
        self.logger = logging.getLogger(__name__)
        self.model = ModelFactory.create_unified_model(detector_name, recognizer_name)
        self.logger.info(f"Loaded model: {detector_name} + {recognizer_name}")
    
    def preprocess_image(self, image, target_size=(100, 100)):
        """图像预处理（适配不同模型输入尺寸）"""
        img = image.convert("RGB").resize(target_size)
        img_array = np.array(img, dtype=np.float32) / 255.0
        return np.expand_dims(img_array, 0)
    
    def process(self, image):
        """处理图像并返回结果"""
        self.logger.info("Starting image processing...")
        
        # 示例：假设先用YOLO检测人脸，再用情感模型预测
        # 实际应用需根据模型类型动态调整流程
        try:
            detection_result = self.model.detect_faces(image)
            for res in detection_result:
                x1, y1, x2, y2 = res['x1'], res['y1'], res['x2'], res['y2']
                    
                face_img = image.crop((x1, y1, x2, y2))
                    
                # 预处理（根据模型配置调整尺寸）
                face_array = self.preprocess_image(face_img, (100, 100))
                    
                    # 情感预测（假设模型是emotion类型）
                emotion_code = self.model.recognize_emotion(face_array)
    
        except Exception as e:
            self.logger.error(f"Processing error: {str(e)}")
            raise
        
        self.logger.info("Processing completed.")
        return emotion_code, detection_result