from main import app
from flask import render_template, redirect, request, url_for, jsonify
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
import os

from models_m import model_loader

class API:
    def __init__(self, app):
        self.app = app
        self._register_APIs()
        
        self.tempToken = None

    def _register_APIs(self):
        self.app.add_url_rule("/", "get_root", self.API_get_root, methods=["GET"])
        self.app.add_url_rule("/v1/detect", "post_detect", self.API_post_detect, methods=["POST"])

    def API_get_root(self):
        return render_template('index.html')
    
    def API_post_detect(self):
        if 'imagen' not in request.files:
            return jsonify({'error': 'No se subió ninguna imagen'})

        file = request.files['imagen']
        if file.filename == '':
            return jsonify({'error': 'Nombre de archivo vacío'})

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Procesar imagen con el modelo
        resultado = detectar_caries(filepath)

        return jsonify({'resultado': resultado})