from flask import Flask
import server 
import os
from data_m.database import TMP_IMGS_PATH

app = Flask(__name__)

if __name__ == "__main__":
    os.makedirs(TMP_IMGS_PATH, exist_ok=True)
    server = server.Server(app)