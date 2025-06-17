import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
import random
import json

def cargar_modelo(ruta_modelo):
    return tf.keras.models.load_model(ruta_modelo)

def preparar_imagen(ruta_imagen, target_size):
    img = image.load_img(ruta_imagen, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

def predecir(modelo, img_preparada):
    pred = modelo.predict(img_preparada)
    return pred

def imagen_aleatoria(directorio):
    archivos = [f for f in os.listdir(directorio) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not archivos:
        raise Exception("No hay imágenes en el directorio.")
    elegido = random.choice(archivos)
    return elegido, os.path.join(directorio, elegido)

def cargar_labels(ruta_json):
    with open(ruta_json, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    ruta_modelo = "TrueDent_v2.h5"
    directorio_imagenes = "../data/src"
    ruta_labels = "../prueba/resultados_dientes.json"
    target_size = (128, 128)

    modelo = cargar_modelo(ruta_modelo)
    labels = cargar_labels(ruta_labels)

    nombre_img, img_path = imagen_aleatoria(directorio_imagenes)
    print("Imagen elegida:", nombre_img)

    img_preparada = preparar_imagen(img_path, target_size)
    prediccion = predecir(modelo, img_preparada)

        # Después de obtener la predicción:
    probabilidad = prediccion[0][0]  # Valor entre 0 y 1
    clase_predicha = 1 if probabilidad >= 0.5 else 0

    print(f"Probabilidad clase 1 (sano): {probabilidad:.4f}")
    print(f"Clase predicha: {clase_predicha}")
