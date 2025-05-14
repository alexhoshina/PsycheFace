"""图像控制器模块。

提供图像处理相关的控制器功能，包括文件上传和WebSocket实时处理接口。
"""

import asyncio
import cv2
import numpy as np
from fastapi import UploadFile, WebSocketDisconnect, WebSocket
from services.image_service import ImageService

class ImageController:
    """图像控制器类，负责处理图像上传和WebSocket实时处理请求。

    提供文件上传和WebSocket实时处理两种接口，支持异步处理图像数据。
    """
    def __init__(self, service: ImageService):
        self.service = service

    async def handle_upload(self, file: UploadFile):
        """处理上传的图像文件。

        Args:
            file: 上传的图像文件

        Returns:
            dict: 处理结果
        """
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return self.service.process(image)
    async def handle_websocket(self, websocket: WebSocket):
        """处理WebSocket连接，实时处理图像数据。

        Args:
            websocket: WebSocket连接实例
        """
        await websocket.accept()
        try:
            while True:
                image_data = await websocket.receive_bytes()
                nparr = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                predictions = await asyncio.to_thread(
                    self.service.process, image
                )
                await websocket.send_json(predictions)
        except WebSocketDisconnect:
            pass
        except (ValueError, IOError, RuntimeError) as e:
            await websocket.send_json({
                "error": f"处理错误: {str(e)}",
                "code": "PROCESSING_ERROR"
            })
        finally:
            await websocket.close()
