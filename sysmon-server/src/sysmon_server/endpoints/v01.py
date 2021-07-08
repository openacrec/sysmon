from flask import request

from sysmon_server.client import Client


def accept_post():
    """
    Handles incoming json data. Save's each json into a file. Separately saves
    the machines names to handle the template for new, unknown hosts.

    :return:
    """
    if request.is_json:
        req = request.get_json()
        # Add the address of the remote
        # Needed to have address for remote execution from client
        req["address"] = request.remote_addr
        client = Client(req)
        client.save_file()

        return "Received!", 200
    else:
        return "Request was not JSON", 400
