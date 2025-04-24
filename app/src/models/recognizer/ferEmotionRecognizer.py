import cv2
import numpy as np
import tensorflow as tf

from src.models.base import EmotionRecognitionModel
from src.models.factory import ModelFactory

@ModelFactory.register_recognizer("fer_1", model_path="fer_v1.h5", input_shape=(100, 100, 3))
class FEREmotionRecognizer(EmotionRecognitionModel):
    """FER情感识别实现"""
    def __init__(self, model_path: str, input_shape: tuple):
        self.model = tf.keras.models.load_model(model_path)
        self.input_shape = input_shape
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """预处理图像"""
        image = cv2.resize(image, (self.input_shape[1], self.input_shape[0]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype(np.float32) / 255.0
        # 检查图片维度是否符合模型要求input_shape[2]
        return image
    
    def recognize_emotion(self, face_image: np.ndarray) -> int:
        input_array = self.preprocess_image(face_image)
        prediction = self.model.predict(input_array)
        return np.argmax(prediction)