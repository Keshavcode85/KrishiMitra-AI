from flask import Flask
from pymongo import MongoClient
import os

def create_app():
    app = Flask(__name__)

    # Secret Key
    app.secret_key = "krishimitra_secret_key"

    # Upload Folder Config
    app.config['UPLOAD_FOLDER'] = 'static/uploads'

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # MongoDB Connection
    mongo_uri = "mongodb+srv://krishimitra:keshav1234@krishimitracluster.xt6kwrj.mongodb.net/?appName=KrishiMitraCluster"
    client = MongoClient(mongo_uri)
    app.db = client["krishimitra_db"]
    print(client.list_database_names())

    # Register Blueprint
    from .routes import main
    app.register_blueprint(main)

    return app