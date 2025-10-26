from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # nano modeli

model.train(
    data='data.yaml',
    epochs=50,
    imgsz=640
)
