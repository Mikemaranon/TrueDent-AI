import os
import json

USER_FILE = "users.json"

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
    
    # ===================================== 
    #           USERS MANAGEMENT
    # =====================================
    
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
    
