import jwt
import zipfile
from flask import render_template, redirect, request, url_for, jsonify, send_file
from user_m.user_manager import UserManager
from data_m.database import Database, USERNAME, PASSWORD
from main import app
import os
import json

class AppRoutes:
    def __init__(self, app, user_manager: UserManager, database: Database):
        self.app = app
        self.user_manager = user_manager
        self.database = database
        self._register_routes()
        self._register_APIs()
    
    def get_request_token(self):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            return token
    
        return None
    
    def check_auth(self):
        token = self.get_request_token()
        return token

    def check_user(self):
        token = self.check_auth()
        if token:
            user = self.user_manager.get_user(token)
            if user:
                return user
        return None
    
    # ==================================================================================
    #                     REGISTERING ROUTES AND APIs
    #
    #            [_register_routes]     instance of every basic route 
    #            [_register_APIs]       instance of every API
    # ================================================================================== 

    def _register_routes(self):
        self.app.add_url_rule("/", "home", self.get_home, methods=["GET"])
        self.app.add_url_rule("/index", "index", self.get_index)
        self.app.add_url_rule("/login", "login", self.get_login, methods=["GET", "POST"])
        self.app.add_url_rule("/logout", "logout", self.get_logout, methods=["POST"])

    def _register_APIs(self):        
        self.app.add_url_rule("/api/post-result", "post_result", self.API_post_result, methods=["POST"])
        self.app.add_url_rule("/api/get-image", "get_image", self.API_get_image, methods=["GET"])
        self.app.add_url_rule("/api/check", "check", self.API_check, methods=["GET"])
        self.app.add_url_rule("/api/download/jsons", "download_jsons", self.API_download_jsons, methods=["GET"])

    # ==================================================================================
    #                           BASIC ROUTINGS URLs
    #
    #            [get_home]             check user and redirect to get_index
    #            [get_index]            go to index.html
    #            [get_login]            log user and send his token
    #            [get_logout]           log user out, send to index.html 
    # ================================================================================== 
    
    def get_index(self):
        return render_template("index.html")
    
    def get_home(self):
        
        user = self.check_user()
        if user:            
            return redirect(url_for("index"))  # Redirect to index.html
        return render_template("login.html")

    def get_login(self):
        error_message = None
        if request.method == "POST":
            data = request.get_json()

            username = data.get("username")
            password = data.get("password")

            token = self.user_manager.login(username, password)
            if token:
                response = jsonify({"token": token})
                return response
            
            error_message = "incorrect user data, try again"

        return render_template("login.html", error_message=error_message)

    def get_logout(self):
        
        token = self.get_request_token()
        
        self.user_manager.logout(token)
        response = redirect(url_for("login"))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    
    # =========================================
    #       API protocols start from here
    # =========================================
    
    def API_post_result(self):
        user = self.check_user()
        if user:   
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            # Process the data as needed, e.g., save to database
            
            self.database.save_result(user.username, data)
            
            print(f"Received data from {user.username}: {data}")
            
            return jsonify({"status": "success", "message": "Data received"}), 200
        
        return 0
    
    
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data_m", "images")
    SRC_DIR = os.path.join(DATA_DIR, "src")

    def API_get_image(self):
        user = self.check_user()
        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        # Obtenemos el nombre de la imagen actual desde query param opcional
        image_name = request.args.get("image_name")

        # Intentamos obtener la siguiente imagen
        image_path = self.database.get_image(image_name, user.username)
        
        if image_path:
            return jsonify({"image": image_path}), 200
        else:
            return jsonify({"message": "No more images"}), 204

    def API_check(self):
        return jsonify({"status": "ok"}), 200
    
    def API_download_jsons(self):
        zip_path = "/tmp/truedent_jsons.zip"

        base_path = os.path.join(os.getcwd(), "data_m")
        images_path = os.path.join(base_path, "images")

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            # Add users.json
            users_json = os.path.join(base_path, "users.json")
            if os.path.exists(users_json):
                zipf.write(users_json, arcname="users.json")

            # Add all JSON files inside images/
            for filename in os.listdir(images_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(images_path, filename)
                    zipf.write(file_path, arcname=f"images/{filename}")

        return send_file(zip_path, as_attachment=True)
    