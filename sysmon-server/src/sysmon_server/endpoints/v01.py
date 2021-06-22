from flask import request

from sysmon_server.client import Client


def accept_post():
    """
    Handles incoming json data. Save's each json into a file. Separately saves
    the machines names to handle the template for new, unknown hosts.

    :return:
    """
    if request.is_json:
        client = Client(request.get_json())
        client.save_file()
        return "Received!", 200
    else:
        return "Request was not JSON", 400
