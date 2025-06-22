import jwt
import datetime
from werkzeug.security import check_password_hash
from data_m.database import Database
from user_m.user import User

class UserManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, secret_key="your-secret-key"):
        if hasattr(self, 'initialized') and self.initialized:
            return # Already initialized
        # Initialize the singleton instance
        
        self.db = Database()
        self.users = {}  # store users by username
        self.secret_key = secret_key
        self.initialized = True

    def authenticate(self, username: str, password: str):
        user = self.db.get_user(username)

        if user:
            print("Stored hashed password:", user["password"])
            print("Password entered by the user:", password)

            if check_password_hash(user["password"], password):
                return True

        return False
    
    # ========================================================
    #     working with the request to get the token
    # ========================================================
    
    def get_request_token(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            return token
        return None

    def check_user(self, request):
        token = self.get_request_token(request)
        if token:
            user = self.get_user(token)
            if user:
                return user
        return None

    # ========================================================
    #     working with the user login and token generation
    # ========================================================

    def generate_token(self, username: str):
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        payload = {
            'username': username,
            'exp': expiration_time
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def login(self, username: str, password: str):
        if self.authenticate(username, password):
            token = self.generate_token(username)
            user = User(token=token, username=username)
            self.users[username] = user
            return token
        return None

    def logout(self, token):
        username = self._get_username_from_token(token)
        if username and username in self.users:
            del self.users[username]
            return {'status': 'success'}, 200
        return {'status': 'not found'}, 404

    def get_user(self, token):
        username = self._get_username_from_token(token)
        if username:
            user = self.users.get(username)
            if user:
                return user
        return None

    # ========================================================
    #     working with the tokens to extract the username
    # ========================================================

    def _get_username_from_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            username = payload.get('username')
            return username
        
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def get_users(self):
        return self.users