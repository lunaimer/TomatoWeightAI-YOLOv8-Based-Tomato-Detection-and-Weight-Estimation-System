from ultralytics import YOLO

model = YOLO("runs/detect/train3/weights/best.pt")
results = model.predict(source="qrr.jpg", conf=0.1, save=True)
