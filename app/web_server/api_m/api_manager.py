import jwt
import zipfile
from werkzeug.utils import secure_filename
from io import BytesIO
import cv2
from flask import render_template, redirect, request, url_for, jsonify, send_file
from user_m.user_manager import UserManager
from modl_m.model_manager import ModelManager
from data_m.database import Database, USERNAME, PASSWORD, HOME_DIR
import os
import json
import shutil

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ApiManager:
    def __init__(self, app, user_manager: UserManager, database: Database, model_manager: ModelManager):
        self.app = app
        self.user_manager = user_manager
        self.model_manager = model_manager
        self.database = database
        self._register_APIs()
        
        HOME_DIR = "/home/mike/Desktop/codes/projects/AI_PRJ/TrueDent-AI/app/web_server/modl_m"
        # Carpeta para guardar imágenes (crearla si no existe)
        self.upload_folder = os.path.join(HOME_DIR, 'imgs/uploads')
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
    
    # ==================================================================================
    #                     REGISTERING APIs
    # ================================================================================== 

    def _register_APIs(self):
        self.app.add_url_rule("/api/check", "check", self.API_check, methods=["GET"])
        self.app.add_url_rule("/api/register", "register", self.API_register, methods=["POST"])
        self.app.add_url_rule("/api/detect", "detect", self.API_detect, methods=["POST"])
        self.app.add_url_rule("/api/upload-image", "upload_image", self.API_upload_image, methods=["POST"])
    
    # =========================================
    #       API protocols start from here
    # =========================================
        
    # endpoint to check if the API is working
    def API_check(self):
        return jsonify({"status": "ok"}), 200
    
    def API_register(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        users = self.database.load_users()  # Ensure users are loaded before checking
        # Check if the user already exist
        if username in users:
            return jsonify({"error": "User already exist"}), 400

        self.database.add_user(username, password)
        return jsonify({"message": "User registered successfully"}), 201
    
    def API_detect(self):
        # This is a placeholder for the detect API
        # Implement the detection logic here
        return jsonify({"message": "Detection API not implemented yet"}), 501
    
    def API_upload_image(self):
        if 'imagen' not in request.files:
            return jsonify({'error': 'No se encontró el archivo'}), 400
        
        file = request.files['imagen']  

        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        if file and allowed_file(file.filename):
            predictions_folder = os.path.join(HOME_DIR, 'imgs/predictions')
            if os.path.exists(predictions_folder):
                shutil.rmtree(predictions_folder)
            
            filename = 'RADIO.jpg' 
            filepath = os.path.join(self.upload_folder, filename)
            file.save(filepath)

            processed_image_np = self.model_manager.inference_v1()

            # 2. Verificar si se obtuvo una imagen procesada
            if processed_image_np is None:
                # Manejar el caso donde no se pudo procesar la imagen (ej. no se detectaron dientes)
                return jsonify({'error': 'No se pudo procesar la imagen o no se detectaron dientes.'}), 500

            success, encoded_image = cv2.imencode('.png', processed_image_np)

            if not success:
                return jsonify({'error': 'Fallo al codificar la imagen procesada.'}), 500

            # Crear un objeto BytesIO para enviar los bytes de la imagen
            image_bytes = BytesIO(encoded_image.tobytes())

            # 4. Devolver la imagen usando send_file
            # El mimetype debe coincidir con el formato de la imagen (ej. 'image/png')
            # Puedes usar un nombre de archivo dinámico si lo deseas.
            return send_file(
                image_bytes,
                mimetype='image/png',
                as_attachment=False, # True si quieres que se descargue, False para mostrarla en el navegador
                download_name=f"processed_{filename}.png" # Nombre sugerido para la descarga
            )
            
        else:
            return jsonify({'error': 'Extensión de archivo no permitida'}), 400