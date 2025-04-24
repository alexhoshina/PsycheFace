import cv2
import numpy as np
import tensorflow as tf

from src.models.base import EmotionRecognitionModel
from src.models.factory import ModelFactory

@ModelFactory.register_recognizer("fer_1", model_path="fer_v1.h5")
class FEREmotionRecognizer(EmotionRecognitionModel):
    """FER情感识别实现"""
    def __init__(self, model_path: str):
        self.model = tf.keras.models.load_model(model_path)
    
    def recognize_emotion(self, face_image: np.ndarray) -> int:
        # 预处理（假设输入尺寸为100x100）
        resized = cv2.resize(face_image, (100, 100))
        normalized = resized / 255.0
        input_array = np.expand_dims(normalized, axis=0)
        prediction = self.model.predict(input_array)
        return np.argmax(prediction)