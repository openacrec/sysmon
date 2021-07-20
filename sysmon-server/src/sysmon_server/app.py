import warnings
from pathlib import Path
from typing import List

from flask import render_template

from client import Client
from endpoints import legacy, v01, deletions, executions
from sysmon_server import app, DATA_STORAGE
from task_status import TaskStatus


def collect_clients() -> List[Client]:
    """
    Return a list with all clients loaded as a instance of the client class.

    :return: List containing Clients
    """
    clients = []
    files = Path(f"{DATA_STORAGE}")
    for file in files.iterdir():
        # TODO: Add a prefix for clients? and all else to differentiate
        if file.is_file() and not file.name == "execution_status.json":
            clients.append(Client({"name": file.stem}, update=False))
    return clients


@app.route("/")
def sysmon():
    """
    Render a site showing status of all connected clients.

    :return:
    """
    clients = collect_clients()
    # Returns clients that are still alive AND deletes long-gone clients
    alive = [client.name for client in clients if client.updated_in_time()]
    # TODO: What about multiple different stati? E.g. from different sources
    task = TaskStatus()
    return render_template("index.html",
                           clients=clients,
                           alive=alive,
                           task=task)


def check_compatible_endpoint_version():
    raise NotImplementedError


@app.route("/post", methods=['GET', 'POST'])
def legacy_endpoint():
    """
    Redirect endpoint functionality to submodule.

    :return: status code
    """
    warnings.warn("Legacy endpoint was used.", DeprecationWarning)
    return legacy.json_handler()


@app.route("/api/v01", methods=['POST'])
def v01_endpoint():
    """
    Redirect endpoint functionality to submodule.

    :return: status code
    """
    return v01.accept_post()


@app.route("/api/del", methods=['POST'])
def del_endpoint():
    """
    Deletes the current data about the requested client.

    :return: status code
    """
    return deletions.delete_client()


@app.route("/api/executions", methods=['POST'])
def executions_endpoint():
    """
    Deletes the current data about the requested client.

    :return: status code
    """
    return executions.update_status()


if __name__ == '__main__':
    app.run(debug=False, port=5000)
