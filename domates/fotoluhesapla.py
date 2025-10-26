from ultralytics import YOLO
import math
import cv2

model = YOLO("runs/detect/train3/weights/best.pt")

img_path = "qr-test.jpg"
img = cv2.imread(img_path)

results = model(img_path)[0]

boxes = results.boxes
labels = boxes.cls.cpu().numpy()
coords = boxes.xywh.cpu().numpy()

# Etiket isimleri
class_names = ['domates', 'qr']

# QR'ı bul (qr sınıfı = 1)
try:
    qr_box = coords[labels == 1][0]
except IndexError:
    raise Exception("QR kodu tespit edilemedi!")

qr_px = qr_box[2]  # genişlik (px)
mm_per_pixel = 65 / qr_px  # QR kenarı = 50 mm (5 cm)

xyxy = results.boxes.xyxy.cpu().numpy()
domates_sayac = 0

for i, (label, coord, rect) in enumerate(zip(labels, coords, xyxy)):
    if label != 0:
        continue  # sadece domatesleri işle

    domates_sayac += 1
    domates_px = coord[3]  # yükseklik = çap
    domates_diameter_mm = domates_px * mm_per_pixel
    radius_cm = (domates_diameter_mm / 10) / 2

    volume_cm3 = (4 / 3) * math.pi * radius_cm ** 3
    weight_grams = volume_cm3 * 0.96
    weight_text = f"{weight_grams:.1f}g"

    x1, y1, x2, y2 = map(int, rect)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(img, weight_text, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    print(f"{domates_sayac}. domates tahmini ağırlık: {weight_text}")

cv2.imwrite("qr_ile_tahmin.jpg", img)
print("\n✅ Tahmin tamamlandı. 'qr_ile_tahmin.jpg' dosyasına yazıldı.")
