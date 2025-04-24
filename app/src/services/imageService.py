import logging
from src.models.factory import ModelFactory

class ImageService:
    """
    图像处理服务
    负责模型推理和结果整合
    """
    def __init__(self, detector_name: str, recognizer_name: str) -> None:
        self.logger = logging.getLogger(__name__)
        self.model = ModelFactory.create_unified_model(detector_name, recognizer_name)
        self.logger.info(f"Loaded model: 人脸检测模型: {detector_name}, 情感识别模型: {recognizer_name}")
    
    def process(self, image):
        """处理图像并返回结果"""
        self.logger.info("Starting image processing...")
        result = []
        try:
            # 使用统一模型检测人脸位置
            detection_result = self.model.detect_faces(image)
            for res in detection_result:
                face_img = image.crop(res)
                emotion_code = self.model.recognize_emotion(face_img)
                result.append((
                    emotion_code, res[0], res[1], res[2], res[3]
                ))
        except Exception as e:
            self.logger.error(f"Processing error: {str(e)}")
            raise
        
        self.logger.info("Processing completed.")
        return result