from flask import Flask
from pymongo import MongoClient
import os

def create_app():
    app = Flask(__name__)

    # Secret Key from environment
    app.secret_key = os.getenv("SECRET_KEY")

    # Upload Folder
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # MongoDB connection
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    app.db = client["krishimitra_db"]

    from .routes import main
    app.register_blueprint(main)

    return app