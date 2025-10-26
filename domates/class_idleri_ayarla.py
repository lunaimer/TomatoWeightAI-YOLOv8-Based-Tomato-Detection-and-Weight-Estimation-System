import os

# Etiket klasörünün yolu (gerekirse tam yol da verebilirsin)
labels_dir = 'ttt'

# Tüm .txt dosyalarını gez
for filename in os.listdir(labels_dir):
    if filename.endswith('.txt'):
        file_path = os.path.join(labels_dir, filename)

        with open(file_path, 'r') as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 5:  # class_id x_center y_center width height
                parts[0] = '1'   # class_id'yi 0 yap
                new_lines.append(' '.join(parts) + '\n')

        # Dosyayı güncelle
        with open(file_path, 'w') as file:
            file.writelines(new_lines)

print("Tüm class ID'leri 0 olarak güncellendi.")
