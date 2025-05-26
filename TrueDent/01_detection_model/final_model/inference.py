import os
import cv2
import random
import json
from pathlib import Path
from ultralytics import YOLO
from collections import Counter


def get_model(model_path: str) -> YOLO:
    return YOLO(model_path)


def load_log(log_path: str) -> dict:
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            return json.load(f)
    return {"inferences": 0, "results": {}}


def save_log(log_data: dict, log_path: str) -> None:
    with open(log_path, "w") as f:
        json.dump(log_data, f, indent=4)


def ensure_output_folder(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def get_random_images(input_folder: str, count: int = 3) -> list:
    img_files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]
    return random.sample(img_files, min(count, len(img_files)))


def read_image(img_path: str):
    img = cv2.imread(img_path)
    if img is None:
        print(f"❌ No se pudo leer {img_path}")
    return img


def predict_image(model: YOLO, img) -> list:
    results = model.predict(source=img, imgsz=960, conf=0.25)
    boxes = results[0].boxes
    if boxes is None or boxes.shape[0] == 0:
        return None
    return results


def labeling_accuracy(detected_teeth: list) -> dict:
    expected_labels = {
        18,17,16,15,14,13,12,11,21,22,23,24,25,26,27,28,
        48,47,46,45,44,43,42,41,31,32,33,34,35,36,37,38
    }

    counts = Counter(detected_teeth)
    correct = sum(1 for label in expected_labels if counts[label] == 1)
    repeated = [label for label in expected_labels if counts[label] > 1]
    missing = [label for label in expected_labels if counts[label] == 0]

    precision = round((correct / len(expected_labels)) * 100, 2)

    return {
        "precision": precision,
        "repeated": repeated,
        "missing": missing
    }


def update_log(log_data: dict, img_name: str, accuracy: dict) -> str:
    log_data["inferences"] += 1
    img_id = f"image_{log_data['inferences']}"
    log_data["results"][img_id] = {
        "file": img_name,
        "precision": f"{accuracy['precision']:.2f}",
        "repeated": str(len(accuracy['repeated'])),
        "missing": list(map(str, accuracy['missing']))
    }
    return img_id


def draw_and_save_results(results, output_path: str, img_name: str) -> None:
    annotated = results[0].plot()
    out_file = os.path.join(output_path, f"pred_{img_name}")
    cv2.imwrite(out_file, annotated)
    print(f"✅ Imagen guardada: {out_file}")


def main():
    model_path = "/home/mike/Desktop/codes/projects/AI_PRJ/TrueDent-AI/TrueDent/01_detection_model/final_model/TrueDent_v1.onnx"
    input_folder = "/home/mike/Desktop/codes/projects/AI_PRJ/TrueDent-AI/TrueDent/01_detection_model/data/yolo_train_dataset/test/images"
    output_folder = "/home/mike/Desktop/codes/projects/AI_PRJ/TrueDent-AI/TrueDent/01_detection_model/final_model/predictions"
    log_path = os.path.join(output_folder, "inference_log.json")

    ensure_output_folder(output_folder)
    model = get_model(model_path)
    log_data = load_log(log_path)
    selected_imgs = get_random_images(input_folder)

    for img_name in selected_imgs:
        print(f"🦷 Procesando {img_name}...")
        img_path = os.path.join(input_folder, img_name)
        img = read_image(img_path)
        if img is None:
            continue

        results = predict_image(model, img)
        if not results:
            print(f"⚠️ No se detectó nada en {img_name}")
            continue

        detected_labels = results[0].boxes.cls.cpu().numpy().astype(int).tolist()
        accuracy = labeling_accuracy(detected_labels)
        update_log(log_data, img_name, accuracy)
        save_log(log_data, log_path)
        draw_and_save_results(results, output_folder, img_name)

    print("🏁 Listo. Solo se procesaron 3 imágenes.")

if __name__ == "__main__":
    main()
