from ultralytics import YOLO
import cv2
import math
import time
import os
import platform

# YOLO modelini yükle
model = YOLO("runs/detect/train3/weights/best.pt")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera açılamadı.")
    exit()

class_names = ['domates', 'qr']

son_yazim_zamani = 0
yazim_araligi = 10  # Konsola yazım aralığı: 10 saniye

agirlik_listesi = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)[0]

    boxes = results.boxes
    labels = boxes.cls.cpu().numpy()
    coords = boxes.xywh.cpu().numpy()
    xyxy = boxes.xyxy.cpu().numpy()

    # QR kod var mı kontrol et
    try:
        qr_box = coords[labels == 1][0]
        qr_px = qr_box[2]  # QR genişliği
        mm_per_pixel = 50 / qr_px  # 50 mm gerçek genişlik
        qr_var = True
    except IndexError:
        mm_per_pixel = None
        qr_var = False

    agirlik_listesi.clear()

    for label, coord, rect in zip(labels, coords, xyxy):
        class_id = int(label)
        class_name = class_names[class_id]
        x1, y1, x2, y2 = map(int, rect)

        # Domates ise:
        if class_name == "domates":
            if qr_var:
                domates_px = coord[3]  # dikey uzunluk
                domates_diameter_mm = domates_px * mm_per_pixel
                radius_cm = (domates_diameter_mm / 10) / 2
                volume_cm3 = (4 / 3) * math.pi * radius_cm ** 3
                weight_grams = volume_cm3 * 0.96
                agirlik_listesi.append(weight_grams)

                # Etiket: Ağırlık
                cv2.putText(frame, f"{weight_grams:.1f}g", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                # Etiket: Sadece sınıf adı
                cv2.putText(frame, "domates", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        elif class_name == "qr":
            # QR kutusu mavi çizilsin
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, "qr", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Konsola 10 saniyede bir yaz
    simdi = time.time()
    if simdi - son_yazim_zamani > yazim_araligi:
        son_yazim_zamani = simdi

        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

        if qr_var:
            print("📷 QR VAR → Tahmini Ağırlıklar (g):")
            if agirlik_listesi:
                for i, ag in enumerate(agirlik_listesi, 1):
                    print(f"{i}. domates: {ag:.1f}g")
            else:
                print("Domates tespit edilemedi.")
        else:
            print("👀 QR YOK → Sadece domates tanıma modu aktif.")

    cv2.imshow("Domates Takibi", frame)

    if cv2.waitKey(1) == 27:  # ESC ile çık
        break

cap.release()
cv2.destroyAllWindows()