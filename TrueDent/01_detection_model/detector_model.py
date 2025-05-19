# detector_model.py

import os
import cv2
import torch
import numpy as np
from typing import List, Dict
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.structures.instances import Instances


class ToothDetector:
    def __init__(self, weights_path: str, threshold: float = 0.7, device: str = "auto") -> None:

        model_path = os.path.join(os.path.dirname(__file__), "model", "mask_rcnn_teeth.pth")
        detector = ToothDetector(model_path)

        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file(
            "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
        ))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold
        self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1 # Solo un tipo de objeto (dientes)
        self.cfg.MODEL.WEIGHTS = weights_path

        if device == "auto":
            self.cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.cfg.MODEL.DEVICE = device

        self.predictor = DefaultPredictor(self.cfg)

    def detect(self, image: np.ndarray) -> Instances:
        """
        Detecta dientes en una imagen.

        :param image: Imagen (BGR) como array de NumPy.
        :return: Objeto Instances con pred_boxes, pred_masks, scores, etc.
        """
        return self.predictor(image)["instances"]

    def extract_results(self, instances: Instances) -> List[Dict]:
        """
        Extrae resultados numéricos de las detecciones.

        :param instances: Resultado de self.detect().
        :return: Lista con info por diente: bbox, score, máscara.
        """
        results = []
        for i in range(len(instances)):
            result = {
                "bbox": instances.pred_boxes[i].tensor.cpu().numpy().tolist()[0],
                "score": float(instances.scores[i].cpu()),
                "mask": instances.pred_masks[i].cpu().numpy().astype(bool)
            }
            results.append(result)
        return results

    def extract_tooth_crops(self, image: np.ndarray, instances: Instances, margin: int = 10) -> List[np.ndarray]:
        """
        Recorta imágenes individuales de cada diente detectado.

        :param image: Imagen original (BGR).
        :param instances: Resultado de self.detect().
        :param margin: Pixeles extra alrededor del diente.
        :return: Lista de imágenes (BGR) de cada diente.
        """
        crops = []
        for i in range(len(instances)):
            mask = instances.pred_masks[i].cpu().numpy().astype(np.uint8)
            ys, xs = np.where(mask > 0)
            if len(xs) == 0 or len(ys) == 0:
                continue  # máscara vacía

            x1 = max(xs.min() - margin, 0)
            x2 = min(xs.max() + margin, image.shape[1])
            y1 = max(ys.min() - margin, 0)
            y2 = min(ys.max() + margin, image.shape[0])

            masked = cv2.bitwise_and(image, image, mask=mask)
            crop = masked[y1:y2, x1:x2]
            crops.append(crop)
        return crops

    def detect_from_path(self, image_path: str) -> Dict[str, List]:
        """
        Carga imagen desde disco y retorna detecciones + crops.

        :param image_path: Ruta a la imagen.
        :return: Dict con resultados (bounding boxes, scores, máscaras) y crops.
        """
        image = cv2.imread(image_path)
        instances = self.detect(image)
        results = self.extract_results(instances)
        crops = self.extract_tooth_crops(image, instances)
        return {
            "results": results,
            "crops": crops
        }
