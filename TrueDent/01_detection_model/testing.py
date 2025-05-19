from detector_model import ToothDetector
import cv2

detector = ToothDetector("ruta/al/pesos.pth")
image = cv2.imread("ruta/a/imagen_panoramica.jpg")

instances = detector.detect(image)
crops = detector.extract_tooth_crops(image, instances)

print(f"Detectados {len(crops)} dientes.")
