"""主应用模块。

提供FastAPI应用的主要入口点，包括路由配置、中间件设置和依赖注入。
"""

from fastapi import FastAPI, File, UploadFile, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from services.image_service import ImageService
from controllers.image_controller import ImageController
from controllers.model_controller import ModelController

from utils.logging_utils import setup_logging

app = FastAPI()
setup_logging()  # 初始化日志

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依赖注入工厂
def get_processor(detector_name: str, recognizer_name: str) -> ImageService:
    """创建并返回一个图像服务实例。

    Args:
        detector_name: 人脸检测模型名称
        recognizer_name: 情感识别模型名称

    Returns:
        ImageService: 配置好的图像服务实例
    """
    return ImageService(detector_name, recognizer_name)

def get_controller(detector_name: str, recognizer_name: str) -> ImageController:
    """创建并返回一个图像控制器实例。

    Args:
        detector_name: 人脸检测模型名称
        recognizer_name: 情感识别模型名称

    Returns:
        ImageController: 配置好的图像控制器实例
    """
    processor = get_processor(detector_name, recognizer_name)
    return ImageController(processor)

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    detector_name: str = Query("mock", description="人脸检测模型名称"),
    recognizer_name: str = Query("mock", description="情感识别模型名称"),
):
    """处理上传的图像文件并进行情感预测。

    Args:
        file: 上传的图像文件
        detector_name: 人脸检测模型名称，默认为"mock"
        recognizer_name: 情感识别模型名称，默认为"mock"

    Returns:
        dict: 预测结果或错误信息
    """
    try:
        controller = get_controller(detector_name, recognizer_name) # 获取控制器实例
        predictions = await controller.handle_upload(file)
        return predictions
    except (ValueError, IOError, RuntimeError) as e:
        return {"error": str(e)}, 400

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, 
    detector: str, 
    recognizer: str
):
    """处理WebSocket连接，用于实时情感识别。

    Args:
        websocket: WebSocket连接实例
        detector: 人脸检测模型名称
        recognizer: 情感识别模型名称
    """
    controller = get_controller(detector, recognizer)
    await controller.handle_websocket(websocket)

@app.get("/models")
async def get_models():
    """获取可用的模型列表。

    Returns:
        list: 包含所有可用模型的列表
    """
    controoler = ModelController()
    return controoler.handle_get_models()
