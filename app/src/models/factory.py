from src.models.unifiedModel import UnifiedModel
from src.models.base import EmotionRecognitionModel, FaceDetectionModel

from typing import Tuple, Type, Dict

class ModelFactory:
    """模型工厂：使用注册表管理模型"""
    _detector_registry: Dict[str, Tuple[Type[FaceDetectionModel], Dict]] = {}
    _recognizer_registry: Dict[str, Tuple[Type[EmotionRecognitionModel], Dict]] = {}
    
    """模型工厂：直接返回完整的统一模型"""
    @classmethod
    def create_unified_model(cls, detector_name: str, recognizer_name: str) -> UnifiedModel:
        detector = cls.create_detector(detector_name)
        recognizer = cls.create_recognizer(recognizer_name)
        return UnifiedModel(detector, recognizer)
    
    @classmethod
    def register_detector(cls, name: str, **kwargs):
        """装饰器：注册检测模型并传递参数"""
        def decorator(model_class: Type[FaceDetectionModel]):
            # 将参数保存到注册表
            cls._detector_registry[name] = (model_class, kwargs)
            return model_class
        return decorator
    
    @classmethod
    def register_recognizer(cls, name: str, **kwargs):
        """装饰器：注册识别模型"""
        def decorator(model_class: Type[EmotionRecognitionModel]):
            cls._recognizer_registry[name] = (model_class, kwargs)
            return model_class
        return decorator
    
    @classmethod
    def create_detector(cls, name: str) -> FaceDetectionModel:
        """根据参数创建实例"""
        model_info = cls._detector_registry.get(name)
        if not model_info:
            raise ValueError(f"Unknown detector: {name}")
        model_class, kwargs = model_info
        return model_class(**kwargs)
    
    @classmethod
    def create_recognizer(cls, name: str) -> EmotionRecognitionModel:
        """通过名称创建识别模型"""
        model_info = cls._recognizer_registry.get(name)
        if not model_info:
            raise ValueError(f"Unknown recognizer: {name}")
        model_class, kwargs = model_info
        return model_class(**kwargs)
    
    @classmethod
    def get_detector_names(cls) -> Dict[str, str]:
        """获取所有检测器名称"""
        return list(cls._detector_registry.keys())
    
    @classmethod
    def get_recognizer_names(cls) -> Dict[str, str]:
        """获取所有识别器名称"""
        return list(cls._recognizer_registry.keys())