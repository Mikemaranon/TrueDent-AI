import os

from modl_m.models.TD_V1 import V1_main
from modl_m.models.TD_V2 import V2_main

HOME_DIR = "/home/mike/Desktop/codes/projects/AI_PRJ/TrueDent-AI/app/web_server/modl_m"

class ModelManager:
    def __init__(self):
        print("ModelManager initialized.")

    def inference_v1(self):
        # TrueDent_V1 inference logic
        
        print("Running inference for TrueDent_V1 model...")
        V1_main()
        
    def inference_v2(self):
        # TrueDent_V2 inference logic
        
        results = []
        print(f"Running inference for TrueDent_V2 model with image")
        for img in os.listdir(HOME_DIR + "/imgs/predictions/isolated_teeth"):
            results.append(V2_main(img))
        return results
    
    