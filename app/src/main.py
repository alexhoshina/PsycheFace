from fastapi import FastAPI, File, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from .controllers.image_controller import ImageProcessingController
from .services.image_processor import ImageProcessor
from .utils.logging_utils import setup_logging
from .config import Config

app = FastAPI()
setup_logging()  # 初始化日志

# CORS配置（开发环境）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依赖注入工厂
def get_processor(detector_name: str, recognizer_name: str) -> ImageProcessor:
    return ImageProcessor(detector_name, recognizer_name)

def get_controller(detector_name: str, recognizer_name: str) -> ImageProcessingController:
    processor = get_processor(detector_name, recognizer_name)
    return ImageProcessingController(processor)

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    detector_name: str = Query("mock", description="人脸检测模型名称"),
    recognizer_name: str = Query("mock", description="情感识别模型名称"),
):
    try:
        
        controller = get_controller(detector_name, recognizer_name) # 获取控制器实例
        predictions = await controller.handle_upload(file)
        print(predictions)
        return {"result": predictions}
    except Exception as e:
        return {"error": str(e)}, 400

# WebSocket端点（示例）
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         controller = get_controller("emotion_recognition")
#         predictions = await controller.handle_websocket(data)
#         await websocket.send_json(predictions)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)