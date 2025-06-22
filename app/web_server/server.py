import json, os
from flask import Flask
from data_m.database import Database
from user_m.user_manager import UserManager
from api_m.api_manager import ApiManager
from app_routes import AppRoutes

class Server:
    def __init__(self, app: Flask):
        self.app = app
        self.app.secret_key = os.urandom(24)
        
        self.database = self.ini_database()
        self.user_manager = self.ini_user_manager()
        self.app_routes = self.ini_app_routes()
        self.api_manager = self.ini_api_manager()

        # Clave secreta para la sesión
        app.secret_key = os.urandom(24)

        # render.com configuration
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=True, host='0.0.0.0', port=port)
        
    def ini_database(self):
        return Database()

    def ini_user_manager(self):
        return UserManager()
    
    def ini_app_routes(self):
        return AppRoutes(self.app, self.user_manager, self.database)
    
    def ini_api_manager(self):
        return ApiManager(self.app, self.user_manager, self.database)
    
    