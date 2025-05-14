"""模型服务模块。

提供模型管理服务，包括获取可用模型列表等功能。
"""

# type: ignore
from models.factory import ModelFactory

class ModelService:
    """模型服务类，用于获取和管理可用的模型列表。"""
    def get_list(self):
        """获取所有可用的检测器和识别器模型列表。

        Returns:
            tuple: 包含检测器列表和识别器列表的元组
        """
        detector_names = ModelFactory.get_detector_names()
        recognizer_names = ModelFactory.get_recognizer_names()
        return detector_names, recognizer_names 