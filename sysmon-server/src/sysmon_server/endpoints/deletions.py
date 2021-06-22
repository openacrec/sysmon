from sysmon_server import DATA_STORAGE
from flask import request
from werkzeug.utils import secure_filename
import pathlib


def delete_client():
    if request.is_json:
        json_data = request.get_json()
        filename = secure_filename(json_data["name"])
        pathlib.Path(f"{DATA_STORAGE}/{filename}.json").unlink()
        return "Deletion successful", 200
