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

def update_log(log_data: dict, img_name: str, accuracy: dict) -> None:
    log_data["inferences"] += 1
    img_id = f"image_{log_data['inferences']}"
    log_data["results"][img_id] = {
        "file": img_name,
        "precision": f"{accuracy['precision']:.2f}",
        "repeated": list(map(str, accuracy['repeated'])),
        "missing": list(map(str, accuracy['missing']))
    }

def save_log(log_data: dict, log_path: str) -> None:
    with open(log_path, "w") as f:
        json.dump(log_data, f, indent=4)

def ensure_output_folder(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def get_random_images(input_folder: str, count: int) -> list:
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
    
    print("🦷 Detección completada: ", results[0])
    return results

def labeling_accuracy(detected_teeth: list[int]) -> dict:
    expected_labels = {
        18,17,16,15,14,13,12,11,21,22,23,24,25,26,27,28,
        48,47,46,45,44,43,42,41,31,32,33,34,35,36,37,38
    }

    detected_set = set(detected_teeth)
    
    from collections import Counter
    counts = Counter(detected_teeth)

    repeated = []
    for label, count in counts.items():
        if count > 1:
            repeated.extend([label] * (count - 1))

    repeated = sorted(repeated)
    missing = sorted(list(expected_labels - detected_set))
    correct = len(expected_labels) - len(missing)

    precision = round((correct / len(expected_labels)) * 100, 2)

    return {
        "precision": precision,
        "repeated": repeated,
        "missing": missing
    }


def draw_and_save_results(results, output_path: str, img_name: str) -> None:
    annotated = results[0].plot()
    out_file = os.path.join(output_path, f"pred_{img_name}")
    cv2.imwrite(out_file, annotated)
    print(f"✅ Imagen guardada: {out_file}")

def save_yolo_labels(results, img_path: str, label_output_path: str):
    img_name = Path(img_path).stem
    label_file = os.path.join(label_output_path, f"{img_name}.txt")
    boxes = results[0].boxes
    h, w = results[0].orig_shape

    with open(label_file, "w") as f:
        for i in range(len(boxes)):
            cls = int(boxes.cls[i].item())
            xywh = boxes.xywh[i]  # tensor([x_center, y_center, width, height])
            x, y, bw, bh = xywh[0] / w, xywh[1] / h, xywh[2] / w, xywh[3] / h
            f.write(f"{cls} {x:.6f} {y:.6f} {bw:.6f} {bh:.6f}\n")

def save_isolated_teeth(results, img, img_name: str, output_dir: str) -> None:
    boxes = results[0].boxes
    if boxes is None or boxes.shape[0] == 0:
        return

    img_basename = Path(img_name).stem
    h_img, w_img = img.shape[:2]

    for i, box in enumerate(boxes):
        cls = int(box.cls.item())
        xyxy = box.xyxy[0].cpu().numpy().astype(int)  # [x1, y1, x2, y2]
        x1, y1, x2, y2 = xyxy

        box_w, box_h = x2 - x1, y2 - y1

        # Padding según proporción
        if box_h < 2 * box_w:
            pad_top = pad_bottom = pad_left = pad_right = 20
        else:
            pad_top = pad_bottom = 0
            pad_left = pad_right = 20

        # Calculamos crop con padding
        crop_x1 = x1 - pad_left
        crop_y1 = y1 - pad_top
        crop_x2 = x2 + pad_right
        crop_y2 = y2 + pad_bottom

        # Ajustar límites para que no salga del tamaño de la imagen
        crop_x1_clamped = max(0, crop_x1)
        crop_y1_clamped = max(0, crop_y1)
        crop_x2_clamped = min(w_img, crop_x2)
        crop_y2_clamped = min(h_img, crop_y2)

        tooth_crop = img[crop_y1_clamped:crop_y2_clamped, crop_x1_clamped:crop_x2_clamped]

        # En caso de que haya padding fuera de la imagen, lo replicamos
        pad_left_actual = crop_x1_clamped - crop_x1
        pad_top_actual = crop_y1_clamped - crop_y1
        pad_right_actual = crop_x2 - crop_x2_clamped
        pad_bottom_actual = crop_y2 - crop_y2_clamped

        if pad_left_actual > 0 or pad_top_actual > 0 or pad_right_actual > 0 or pad_bottom_actual > 0:
            tooth_crop = cv2.copyMakeBorder(
                tooth_crop,
                top=pad_top_actual,
                bottom=pad_bottom_actual,
                left=pad_left_actual,
                right=pad_right_actual,
                borderType=cv2.BORDER_REPLICATE
            )

        out_path = os.path.join(output_dir, f"{img_basename}_tooth_{cls}_{i}.jpg")
        cv2.imwrite(out_path, tooth_crop)
        print(f"🖼️ Diente aislado guardado: {out_path}")


def main():
    
    # ============ CONFIG AND CONSTANTS ============
    
    IMG_COUNT = 20
    HOME_DIR = "/home/mike/Desktop/codes/projects/AI_PRJ/TrueDent-AI/TrueDent/01_detection_model/"
    RETRAIN = True
    
    model_path = os.path.join(HOME_DIR, "final_model/TrueDent_v1.onnx")
    input_folder = os.path.join(HOME_DIR, "data/yolo_train_dataset/test/images")
    output_folder = os.path.join(HOME_DIR, "final_model/predictions")
    log_path = os.path.join(HOME_DIR, "final_model/inference_log.json")
    
    isolated_teeth_dir = os.path.join(HOME_DIR, "data/isolated_teeth")
    retraining_folder = os.path.join(HOME_DIR, "data/retraining_data/train")
    image_output_dir = os.path.join(retraining_folder, "images")
    label_output_dir = os.path.join(retraining_folder, "labels")
    check_output_dir = os.path.join(retraining_folder, "check")
    

    os.makedirs(image_output_dir, exist_ok=True)
    os.makedirs(label_output_dir, exist_ok=True)
    os.makedirs(check_output_dir, exist_ok=True)

    ensure_output_folder(output_folder)
    model = get_model(model_path)
    log_data = load_log(log_path)
    selected_imgs = get_random_images(input_folder, IMG_COUNT)
    
    # =========== MAIN PROCESS ===========

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

        cls_indices = results[0].boxes.cls.cpu().numpy().astype(int).tolist()

        names_dict = results[0].names
        detected_labels = [int(names_dict[idx]) for idx in cls_indices]
        
        accuracy = labeling_accuracy(detected_labels)
        
        # FILTRO: solo guardamos pseudo-labels si la precisión supera 90%
        if RETRAIN and accuracy["precision"] >= 90 and len(accuracy["repeated"]) == 0:
            img_name = Path(img_path).name
            save_yolo_labels(results, img_path, label_output_dir)
            cv2.imwrite(os.path.join(image_output_dir, img_name), img)
            draw_and_save_results(results, check_output_dir, img_name)
            print(f"📥 Imagen y label guardados para reentrenamiento: {img_name}")
            
            os.makedirs(isolated_teeth_dir, exist_ok=True)
            save_isolated_teeth(results, img, img_name, isolated_teeth_dir)
            print(f"🦷 Dientes aislados guardados en: {isolated_teeth_dir}")
        
        update_log(log_data, img_name, accuracy)
        save_log(log_data, log_path)
        draw_and_save_results(results, output_folder, img_name)

    print("🏁 Listo. Solo se procesaron ", IMG_COUNT, " imágenes.")

if __name__ == "__main__":
    main()
