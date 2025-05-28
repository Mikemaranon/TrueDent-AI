import json, os
from flask import Flask
from data_m.database import Database
from user_m.user_manager import UserManager
from app_routes import AppRoutes

class Server:
    def __init__(self, app: Flask):
        self.app = app
        self.app.secret_key = os.urandom(24)
        
        self.database = self.ini_database()
        self.user_manager = self.ini_user_manager()
        self.app_routes = self.ini_app_routes()

        # Clave secreta para la sesión
        app.secret_key = os.urandom(24)
        
        app.run(debug=True, host='127.0.0.1', port='5000')
        
    def ini_database(self):
        return Database()

    def ini_user_manager(self):
        return UserManager()
    
    def ini_app_routes(self):
        return AppRoutes(self.app, self.user_manager, self.database)