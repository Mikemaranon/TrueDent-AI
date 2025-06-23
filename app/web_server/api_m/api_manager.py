import jwt
import zipfile
from werkzeug.utils import secure_filename
from io import BytesIO
import cv2
from flask import render_template, redirect, request, send_from_directory, url_for, jsonify, send_file
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

            self.model_manager.inference_v1()
            
            return send_from_directory(os.path.join(HOME_DIR, 'imgs/predictions'), 'pred_RADIO.jpg')
            
        else:
            return jsonify({'error': 'Extensión de archivo no permitida'}), 400