import os
import json

USER_FILE = "users.json"
IMGS_PATH = "images/"

# SESSION PARAMS
USERNAME = 'username'
PASSWORD = 'password'

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
            # If user file does not exist, create it with an empty list
            with open(user_file, "w") as f:
                json.dump({
                    "last-image": 0,
                }, f)
            return 0
        
        with open(user_file, "r") as f:
            data = json.load(f)
            return data.get("last-image", 0)  # Returns 0 if key doesn't exist
    
    def get_image(self, image_name: str, username: str):
        images_file = os.path.join(os.path.dirname(__file__), IMGS_PATH, "images.json")
    
        with open(images_file, "r") as f:
            images_list = json.load(f)
        
        if not image_name:
            # If no image provided, return first image
            if images_list:
                return os.path.join(IMGS_PATH, "src", images_list[0])
            return None
        
        try:
            current_index = self.get_user_index(username)
            # If there's a next image, return it
            if current_index < len(images_list) - 1:
                next_image = images_list[current_index + 1]
                return os.path.join(IMGS_PATH, "src", next_image)
            # If we're at the last image, return None or wrap around to first
            return None
        except ValueError:
            # If image not found in list, return first image
            if images_list:
                return os.path.join(IMGS_PATH, "src", images_list[0])
            return None
        
    def post_image(self, image_name: str, username: str, data: dict):
        user_file = os.path.join(os.path.dirname(__file__), IMGS_PATH, username + ".json")
        
        with open(user_file, "r") as f:
            history = json.load(f)
        
        img = "image_" + history.get("last-image")
        
        history[img] = data
        history["last-image"] += 1
        with open(user_file, "w") as f:
            json.dump(history, f)