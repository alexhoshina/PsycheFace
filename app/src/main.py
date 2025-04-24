from fastapi import FastAPI, File, UploadFile, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .services.imageService import ImageService
from .controllers.imageController import ImageController
from .controllers.modelController import ModelController

from .utils.logging_utils import setup_logging

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
    return ImageService(detector_name, recognizer_name)

def get_controller(detector_name: str, recognizer_name: str) -> ImageController:
    processor = get_processor(detector_name, recognizer_name)
    return ImageController(processor)

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    detector_name: str = Query("mock", description="人脸检测模型名称"),
    recognizer_name: str = Query("mock", description="情感识别模型名称"),
):
    try:
        controller = get_controller(detector_name, recognizer_name) # 获取控制器实例
        predictions = await controller.handle_upload(file)
        return {"result": predictions}
    except Exception as e:
        return {"error": str(e)}, 400

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, 
    detector: str, 
    recognizer: str
):
    controller = get_controller(detector, recognizer)
    await controller.handle_websocket(websocket)

@app.get("/models")
async def get_models():
    """获取可用的模型列表"""
    controoler = ModelController()
    return controoler.handle_get_models()