from flask import Flask
from flask_cors import CORS
from server.config import Config


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)


import server.facefolder
import server.queries
