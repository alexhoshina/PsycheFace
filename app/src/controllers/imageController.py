import asyncio
from fastapi import UploadFile, WebSocketDisconnect, WebSocket
from src.services.imageService import ImageService

import asyncio
import cv2
import numpy as np

class ImageController:
    def __init__(self, service: ImageService):
        self.service = service
    
    async def handle_upload(self, file: UploadFile):
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return self.service.process(image)
    
    async def handle_websocket(self, websocket: WebSocket):
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
        except Exception as e:
            await websocket.send_json({
                "error": f"Unexpected error: {str(e)}",
                "code": "INTERNAL_ERROR"
            })
        finally:
            await websocket.close()