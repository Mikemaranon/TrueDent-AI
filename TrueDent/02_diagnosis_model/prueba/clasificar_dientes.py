import cv2
import os
import json

def es_diente_sano(imagen_path, umbral_blanco=200, porcentaje_sano=0.3):
    imagen = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        return {"error": "No se pudo cargar la imagen"}

    total_pixeles = imagen.size
    blancos = cv2.countNonZero(cv2.inRange(imagen, umbral_blanco, 255))
    porcentaje_blancos = blancos / total_pixeles

    return {
        "blancos": blancos,
        "total_pixeles": total_pixeles,
        "porcentaje_blancos": round(porcentaje_blancos, 4),
        "salud": "sano" if porcentaje_blancos >= porcentaje_sano else "no sano"
    }

def analizar_dataset(ruta_carpeta):
    resultados = {}
    for archivo in os.listdir(ruta_carpeta):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            ruta_img = os.path.join(ruta_carpeta, archivo)
            resultado = es_diente_sano(ruta_img)
            resultados[archivo] = resultado
    return resultados

if __name__ == "__main__":
    carpeta_imagenes = "src"  # Carpeta donde están las imágenes
    salida_json = "resultados_dientes.json"

    resultados = analizar_dataset(carpeta_imagenes)

    with open(salida_json, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    print(f"Resultados guardados en {salida_json}")
