import os

from flask import Flask

app = Flask(__name__)

DATA_STORAGE = f"{app.instance_path}/data"
os.makedirs(DATA_STORAGE, exist_ok=True)
MACHINE_NAMES_FILE = f"{DATA_STORAGE}/machine_names.json"
