import os
import cv2
import random
from ultralytics import YOLO
from pathlib import Path

# Paths
model_path = "/home/mike/Desktop/codes/projects/AI_PRJ/TrueDent-AI/TrueDent/01_detection_model/final_models/TrueDent_v1.onnx"
input_folder = "/home/mike/Desktop/codes/projects/AI_PRJ/TrueDent-AI/TrueDent/01_detection_model/data/yolo_train_dataset/test/images"
output_folder = "/home/mike/Desktop/codes/projects/AI_PRJ/TrueDent-AI/TrueDent/01_detection_model/final_models/predictions"

# Crear carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Cargar el modelo
model = YOLO(model_path)

# Obtener 3 imágenes aleatorias
img_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
selected_imgs = random.sample(img_files, 3)

# Procesar
for img_name in selected_imgs:
    img_path = os.path.join(input_folder, img_name)
    img = cv2.imread(img_path)

    if img is None:
        print(f"❌ No se pudo leer {img_name}")
        continue

    print(f"🦷 Procesando {img_name}...")

    # Inferencia
    results = model.predict(source=img, imgsz=960, conf=0.25)

    # Verificar detecciones
    boxes = results[0].boxes
    if boxes is None or boxes.shape[0] == 0:
        print(f"⚠️ No se detectó nada en {img_name}")
        continue

    # Dibujar y guardar
    annotated = results[0].plot()
    out_path = os.path.join(output_folder, f"pred_{img_name}")
    cv2.imwrite(out_path, annotated)
    print(f"✅ Imagen guardada: {out_path}")

print("🏁 Listo. Solo se procesaron 3 imágenes.")