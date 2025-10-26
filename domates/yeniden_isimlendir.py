import os

image_dir = 'qr'

# Geçerli uzantılar
image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']

# Tüm görsel dosyalarını al ve sırala
image_files = sorted([
    f for f in os.listdir(image_dir)
    if os.path.splitext(f)[1].lower() in image_exts
])

# Yeniden adlandır
for idx, img in enumerate(image_files, start=1):
    ext = os.path.splitext(img)[1].lower()
    new_name = f"qr_{idx}{ext}"
    os.rename(os.path.join(image_dir, img), os.path.join(image_dir, new_name))

print("Tüm görseller sırayla yeniden adlandırıldı.")
