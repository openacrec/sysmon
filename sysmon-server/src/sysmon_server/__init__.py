import os

from flask import Flask

app = Flask(__name__)

# TODO: Change images dir to something else
# TODO: Use instance path instead of root_path
DATA_STORAGE = f"{app.instance_path}/data"
os.makedirs(DATA_STORAGE, exist_ok=True)
MACHINE_NAMES_FILE = f"{DATA_STORAGE}/machine_names.json"
