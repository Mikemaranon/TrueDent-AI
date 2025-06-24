import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
import random
import json

def load_model(model_path):
    return tf.keras.models.load_model(model_path)

def transform_img(img_path, target_size):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

def predict(model, prepared_img):
    pred = model.predict(prepared_img)
    return pred

def V2_main(img):
    # ============ CONFIG AND CONSTANTS ============
    HOME_DIR = "/home/mike/Desktop/codes/projects/AI_PRJ/TrueDent-AI/app/web_server/modl_m"
    
    model_path = os.path.join(HOME_DIR, "models/TrueDent_v2.h5")
    img_path = os.path.join(HOME_DIR, "imgs/predictions/isolated_teeth", img)
    target_size = (128, 128)

    model = load_model(model_path)

    prepared_img = transform_img(img_path, target_size)
    pred = predict(model, prepared_img)

    # Después de obtener la predicción:
    prob = pred[0][0]  # Valor entre 0 y 1
    p_class = 1 if prob >= 0.5 else 0

    print(f"Probabilidad clase 1 (sano): {prob:.4f}")
    print(f"Clase predicha: {p_class}")
    
    return {
        "image_name": img,
        "confidence": float(prob),
        "predicted_class": int(p_class)
    }
