class User:
    def __init__(self, token, username, session_data=None):
        self.token = token
        self.username = username
        self.session_data = session_data or {}

    def set_session_data(self, key, value):
        self.session_data[key] = value

    def get_session_data(self, key, default=None):
        return self.session_data.get(key, default)

    def clear_session(self):
        self.session_data.clear()