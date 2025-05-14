"""模型控制器模块。

提供模型相关的控制器功能，包括获取可用模型列表等接口。
"""

# type: ignore
from services.model_service import ModelService

class ModelController:
    """模型控制器类，负责处理模型相关的请求。

    提供获取可用模型列表等功能的接口。
    """
    def handle_get_models(self):
        """获取可用的模型列表"""
        model_service = ModelService()
        return model_service.get_list()
