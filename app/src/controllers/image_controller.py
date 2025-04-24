from io import BytesIO
from fastapi import UploadFile
from PIL import Image
import base64
from src.services.image_processor import ImageProcessor

class ImageProcessingController:
    """
    控制器层（依赖注入）
    负责处理HTTP/WebSocket请求
    """
    def __init__(self, processor: ImageProcessor):
        self.processor = processor
    
    async def handle_upload(self, file: UploadFile):
        """处理上传的图片文件"""
        image = Image.open(BytesIO(await file.read()))
        return self.processor.process(image)
    
    async def handle_websocket(self, data: str):
        """处理WebSocket传输的Base64图片"""
        image = self._decode_base64_image(data)
        return self.processor.process(image)
    
    def _decode_base64_image(self, data: str):
        """解析Base64图片数据"""
        if "base64," in data:
            data = data.split("base64,")[1]
        image_bytes = base64.b64decode(data)
        return Image.open(BytesIO(image_bytes))