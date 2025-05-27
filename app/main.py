from flask import Flask
import server 

app = Flask(__name__)

if __name__ == "__main__":
    server = server.Server(app)