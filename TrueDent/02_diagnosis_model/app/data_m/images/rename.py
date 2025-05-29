import os

folder = "/home/mike/Desktop/codes/projects/AI_PRJ/TrueDent-AI/TrueDent/02_diagnosis_model/app/data_m/images/src"  
files = sorted(os.listdir(folder))
files = [f for f in files if os.path.isfile(os.path.join(folder, f))]

# Rename with format image_0001.ext
for i, original_name in enumerate(files, start=1):
    extension = os.path.splitext(original_name)[1]
    new_name = f"image_{i:04d}{extension}"
    
    original_path = os.path.join(folder, original_name)
    new_path = os.path.join(folder, new_name)

    os.rename(original_path, new_path)

print("Renaming completed.")
