import asyncio
from io import BytesIO
from fastapi import UploadFile, WebSocketDisconnect, WebSocket
from PIL import Image
import base64
from src.services.imageService import ImageService

class ImageController:
    """
    控制器层（依赖注入）
    负责处理HTTP/WebSocket请求
    """
    def __init__(self, service: ImageService):
        self.service = service
    
    async def handle_upload(self, file: UploadFile):
        """处理上传的图片文件"""
        image = Image.open(BytesIO(await file.read()))
        return self.service.process(image)
    
    async def handle_websocket(self, websocket: WebSocket):
        """处理WebSocket传输的图片"""
        await websocket.accept()
        try:
            while True:
                # 接收二进制图像数据
                image_data = await websocket.receive_bytes()
                
                try:
                    # 将字节流转换为Image对象
                    image = Image.open(BytesIO(image_data))
                    
                    # 异步执行模型推理
                    predictions = await asyncio.to_thread(
                        self.service.process, image
                    )
                    
                    # 返回成功结果
                    await websocket.send_json({"result": predictions})
                    
                except Exception as e:
                    # 处理图像处理或模型推理错误
                    await websocket.send_json({
                        "error": f"Processing failed: {str(e)}",
                        "code": "PROCESSING_ERROR"
                    })
                    
        except WebSocketDisconnect:
            # 客户端断开连接
            pass
        except Exception as e:
            # 其他未知错误
            await websocket.send_json({
                "error": f"Unexpected error: {str(e)}",
                "code": "INTERNAL_ERROR"
            })
        finally:
            # 确保关闭连接
            await websocket.close()