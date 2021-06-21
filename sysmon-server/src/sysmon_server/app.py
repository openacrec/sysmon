import warnings
from json import load
from pathlib import Path
from typing import List

from flask import render_template

from sysmon_server import app, DATA_STORAGE
from client import Client
from endpoints import legacy, v01


def collect_clients() -> List:
    """
    Return a list with all clients loaded as a instance of the client class.

    :return: List containing Clients
    """
    clients = []
    files = Path(f"{DATA_STORAGE}")
    for file in files.iterdir():
        if file.is_file():
            with open(file) as client_file:
                clients.append(Client(load(client_file)))
    return clients


@app.route("/")
def sysmon():
    """
    Render a site showing status of all connected clients.

    :return:
    """
    clients = collect_clients()
    alive = [client.name for client in clients if client.updated_in_time()]
    return render_template("index.html", hosts=clients, alive=alive)


def check_compatible_endpoint_version():
    raise NotImplementedError


@app.route("/post", methods=['GET', 'POST'])
def legacy_endpoint():
    """
    Redirect endpoint functionality to submodule.

    :return: status code
    """
    warnings.warn("Legacy endpoint.", DeprecationWarning)
    return legacy.json_handler()


@app.route("/api/v01", methods=['POST'])
def v01_endpoint():
    """
    Redirect endpoint functionality to submodule.

    :return: status code
    """
    return v01.accept_post()


if __name__ == '__main__':
    sysmon.run(debug=False, port=5000)
