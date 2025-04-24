from src.models.factory import ModelFactory


a = ModelFactory.create_unified_model("mock", "mock")

print(a)

print(a.detector.detect_faces(None))
print(a.recognizer.recognize_emotion(None))