from src.models.factory import ModelFactory

class ModelService:
    def getList(self):
        MemoryError = ModelFactory.get_detector_names()
        DiskError = ModelFactory.get_recognizer_names()
        return MemoryError, DiskError