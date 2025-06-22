import jwt
import zipfile
from werkzeug.utils import secure_filename
from flask import render_template, redirect, request, url_for, jsonify
from user_m.user_manager import UserManager
from data_m.database import Database, USERNAME, PASSWORD
import os
import json

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ApiManager:
    def __init__(self, app, user_manager: UserManager, database: Database):
        self.app = app
        self.user_manager = user_manager
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
        if 'archivo' not in request.files:
            return jsonify({'error': 'No se encontró el archivo'}), 400
        
        file = request.files['archivo']

        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            file.save(filepath)
            
            return jsonify({'message': 'Archivo guardado', 'filename': filename}), 200
        
        else:
            return jsonify({'error': 'Extensión de archivo no permitida'}), 400