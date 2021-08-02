import json

from flask import request

from sysmon_server import DATA_STORAGE


def update_status():
    """
    Handle status updates about remote execution.

    :return:
    """

    if request.is_json:
        status = request.get_json()
        with open(f"{DATA_STORAGE}/execution_status.json", "w+") as out:
            json.dump(status, out)

        return "Received!", 200
    else:
        return "Request was not JSON", 400
