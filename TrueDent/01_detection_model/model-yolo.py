import os
import psutil
import shutil
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
from PIL import Image
from skimage import exposure

class GPUConfigurator:
    def __init__(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Reduce TensorFlow logging
        import tensorflow as tf
        self.tf = tf
        self._configure_tensorflow()
    
    def _configure_tensorflow(self):
        self.tf.compat.v1.logging.set_verbosity(self.tf.compat.v1.logging.ERROR)
        gpus = self.tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    self.tf.config.experimental.set_memory_growth(gpu, True)
            except RuntimeError as e:
                print(e)
    
    def print_gpu_info(self):
        print("Num GPUs Available: ", len(self.tf.config.list_physical_devices('GPU')))
        gpus = self.tf.config.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    self.tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = self.tf.config.list_logical_devices('GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
            except RuntimeError as e:
                print(e)
        
        print("====================================================================")     
        print("||                     DRIVERS AND GPU INFO                       ||")       
        print("====================================================================")      
        print("")
        
        gpu_info = os.popen('nvidia-smi').read()
        if 'failed' in gpu_info.lower():
            print('Not connected to a GPU')
        else:
            print(gpu_info)


class SystemMonitor:
    @staticmethod
    def get_ram_usage_gb():
        return psutil.virtual_memory().used / (1024 ** 3)
    
    @staticmethod
    def print_memory_info():
        memory = psutil.virtual_memory()
        print(f"Total Memory: {memory.total / (1024 ** 3):.2f} GB")
        print(f"Used Memory: {memory.used / (1024 ** 3):.2f} GB")
        print(f"Free Memory: {memory.available / (1024 ** 3):.2f} GB")
        print(f"Memory Usage: {memory.percent}%")
    
    @staticmethod
    def print_system_info():
        ram_gb = psutil.virtual_memory().total / 1e9
        print(f'Your runtime has {ram_gb:.1f} gigabytes of available RAM\n')
        if ram_gb < 20:
            print('Not using a high-RAM runtime')
        else:
            print('You are using a high-RAM runtime!')


class YOLOModelHandler:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.model = None
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, path):
        self.model = YOLO(path)
    
    def train(self, data_yaml_path, epochs=150, imgsz=960, batch=16, name='TrueDentYOLOv8m', lr0=0.01, lrf=0.01, warmup_epochs=3, patience=50, device=0):
        if not self.model:
            raise ValueError("Modelo no cargado. Usa load_model() antes de entrenar.")
        results = self.model.train(
            data=data_yaml_path,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            name=name,
            lr0=lr0,
            lrf=lrf,
            warmup_epochs=warmup_epochs,
            patience=patience,
            device=device,
        )
        return results
    
    def validate(self):
        if not self.model:
            raise ValueError("Modelo no cargado. Usa load_model() antes de validar.")
        metrics = self.model.val()
        return metrics
    
    def export_onnx(self, export_dir='final_models', export_name='TrueDent_v1.onnx'):
        if not self.model:
            raise ValueError("Modelo no cargado. Usa load_model() antes de exportar.")
        
        os.makedirs(export_dir, exist_ok=True)
        exported_model_path = self.model.export(format='onnx')
        
        onnx_generated = os.path.splitext(self.model_path)[0] + '.onnx'
        onnx_target_path = os.path.join(export_dir, export_name)
        
        if os.path.exists(onnx_generated):
            shutil.move(onnx_generated, onnx_target_path)
            print(f"✅ Modelo exportado a: {onnx_target_path}")
        else:
            print("❌ No se encontró el archivo .onnx generado.")
        return onnx_target_path


def main():
    print("=== Configurando GPU ===")
    gpu_config = GPUConfigurator()
    gpu_config.print_gpu_info()
    
    print("\n=== Info de sistema ===")
    sys_mon = SystemMonitor()
    print(f"RAM Usage: {sys_mon.get_ram_usage_gb():.2f} GB")
    sys_mon.print_memory_info()
    sys_mon.print_system_info()
    
    print("\n=== Configuración y verificación de ultralytics ===")
    import ultralytics
    ultralytics.checks()
    
    # Entrenamiento del modelo YOLO
    print("\n=== Entrenando modelo YOLO ===")
    model_path = "yolov8m.pt"
    data_yaml_path = 'data/yolo_train_dataset/data.yaml'
    
    yolo_handler = YOLOModelHandler(model_path)
    yolo_handler.train(data_yaml_path=data_yaml_path, epochs=150, imgsz=960, batch=16, name='TrueDentYOLOv8m',
                       lr0=0.01, lrf=0.01, warmup_epochs=3, patience=50, device=0)
    
    print("\n=== Validando modelo ===")
    metrics = yolo_handler.validate()
    print(metrics)
    
    # Exportar a ONNX
    print("\n=== Exportando modelo a ONNX ===")
    pt_path = '/home/mike/Desktop/codes/projects/AI_PRJ/TrueDent-AI/runs/detect/TrueDentYOLOv8m4/weights/best.pt'
    yolo_handler = YOLOModelHandler(pt_path)
    yolo_handler.export_onnx(export_dir='final_models', export_name='TrueDent_v2.onnx')


if __name__ == "__main__":
    main()
