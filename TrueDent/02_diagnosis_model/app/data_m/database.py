import os
import json

USER_FILE = "users.json"
IMGS_PATH = "images/"

# SESSION PARAMS
USERNAME = 'username'
PASSWORD = 'password'

TOTAL_IMAGES = 1152
IMAGE_PREFIX = "image_"
IMAGE_EXT = ".jpg" 

class Database:
    
    # static ini
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.users_file = os.path.join(os.path.dirname(__file__), USER_FILE)
    
    # ================= USERS ================= #
    
    def load_users(self):
        with open(self.users_file, "r") as f:
            return json.load(f)

    def save_users(self, users):
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=4)
            
    def add_user(self, username: str, password: str):
        users = self.load_users()
        users[username] = {"password": password}
        self.save_users(users)

    def get_user(self, username: str):
        users = self.load_users()
        return users.get(username)
    
    # ================= IMAGES ================= #
    
    def get_user_index(self, username: str):
        user_file = os.path.join(os.path.dirname(__file__), IMGS_PATH, username + ".json")

        if not os.path.exists(user_file):
            with open(user_file, "w") as f:
                json.dump({"last-image": 0}, f)
            return 0

        with open(user_file, "r") as f:
            data = json.load(f)
            return data.get("last-image", 0)

    
    def get_image(self, username: str):
        index = self.get_user_index(username)

        if index < TOTAL_IMAGES:
            next_image_name = f"{IMAGE_PREFIX}{(index + 1):04d}{IMAGE_EXT}"
            return os.path.join(IMGS_PATH, "src", next_image_name)
        
        return None  # Ya no hay más imágenes

        
    def post_image(self, image_name: str, username: str, data: dict):
        user_file = os.path.join(os.path.dirname(__file__), IMGS_PATH, username + ".json")

        with open(user_file, "r") as f:
            history = json.load(f)

        # Guardamos la respuesta bajo el nombre de imagen
        history[image_name] = data

        # Avanzamos el índice
        history["last-image"] += 1

        with open(user_file, "w") as f:
            json.dump(history, f, indent=4)
