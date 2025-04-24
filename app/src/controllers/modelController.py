from src.services.modelService import ModelService

class ModelController:
    def handle_get_models(self):
        """获取可用的模型列表"""
        modelService = ModelService()
        return modelService.getList()