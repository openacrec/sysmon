from flask import request

from sysmon_server.client import Client


def delete_client():
    """
    Handles deletion requests.

    :return:
    """
    if request.is_json:
        client = Client(request.get_json(), limited=True)
        client.delete_file()
        return "Deletion successful", 200
