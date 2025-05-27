import json, os
from flask import Flask
from app.api import API 

class Server:
    def __init__(self, app: Flask):
        self.app = app
        self.app.secret_key = os.urandom(24)
        
        self.routes = self.ini_api()

        # Clave secreta para la sesión
        app.secret_key = os.urandom(24)
        
        app.run(debug=True)
    
    def ini_api(self):
        return API()