import cv2
import numpy as np
import tensorflow as tf

from src.models.base import EmotionRecognitionModel
from src.models.factory import ModelFactory

@ModelFactory.register_recognizer("fer_1", model_path="fer_v1.h5", input_shape=(100, 100, 3))
class FEREmotionRecognizer(EmotionRecognitionModel):
    def __init__(self, model_path: str, input_shape: tuple):
        self.model = tf.keras.models.load_model(model_path)
        self.input_shape = input_shape
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        # 调整图像大小以适应模型输入要求
        image_resized = cv2.resize(image, (self.input_shape[1], self.input_shape[0]))
        image_resized = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)  # 如果模型需要RGB格式
        image_resized = image_resized.astype(np.float32) / 255.0  # 归一化
        return np.expand_dims(image_resized, axis=0)  # 增加batch维度

    def recognize_emotion(self, face_image: np.ndarray) -> int:
        input_array = self.preprocess_image(face_image)
        prediction = self.model.predict(input_array)
        return np.argmax(prediction)