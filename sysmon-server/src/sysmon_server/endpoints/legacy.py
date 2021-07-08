from time import strptime, mktime
from typing import Dict

from flask import request

from sysmon_server.client import Client


def to_new_json_format(client_json: Dict):
    json = {
        "name": client_json["machine_name"],
        "endpoint_version": "legacy",
        "address": client_json["address"],
        "time": client_json["time"][-1],
        "timestamp": str_to_unix(client_json["time"][-1], "%Y-%m-%d %H:%M:%S"),
        "cpu": client_json["cpu"][-1],
        "memory": client_json["memory"][-1]
    }
    # Catch: No interval sent or list sent instead of int
    try:
        json["interval"] = client_json["interval"]
        if type(json["interval"]) == list:
            json["interval"] = json["interval"][-1]
    except KeyError:
        json["interval"] = 86400

    # Previously instead of None the whole gpu key was deleted
    # if no gpu was found
    try:
        json["gpu"] = client_json["gpu"][-1]
    except KeyError:
        json["gpu"] = None
    return json


def str_to_unix(time_string, time_format):
    """
    Tries to convert the time (given as string) to time epoch.

    Only for legacy purpose. Deprecated.

    :param time_string: a string in a valid format
    :param time_format: the format used for the string
    :return: time as seconds
    """
    try:
        time = strptime(time_string, time_format)
        time = mktime(time)
    except ValueError:
        time = None
    return time


def update_clients_and_times(req, names_json):
    """
    New clients should go straight into the names list,
    while old clients get there "last seen" time updated.

    :param req: the json with the new client info
    :param names_json: the json with the list of names and "last seen" times
    :return: json with updated values for names or times
    """
    new_name = req["machine_name"]
    new_time = req["time"][-1]
    machine_names = names_json["names"]
    machine_times = names_json["times"]

    if new_name not in machine_names:
        machine_names.append(new_name)
        machine_times.append(new_time)
        names_json["names"] = machine_names
        names_json["times"] = machine_times
    else:
        updated_times = []
        for name, time in zip(machine_names, machine_times):
            if name == new_name:
                updated_times.append(new_time)
            else:
                updated_times.append(time)
        names_json["times"] = updated_times
    return names_json


def json_handler():
    """
    Handles incoming json data. Save's each json into a file. Separately saves
    the machines names to handle the template for new, unknown hosts.

    :return:
    """
    if request.method == 'POST':
        if request.is_json:
            req = request.get_json()
            req["address"] = request.remote_addr
            req = to_new_json_format(req)

            client = Client(req)
            client.save_file()

            return "Received!", 200
        else:
            return "Request was not JSON", 400
    else:
        return ("<p>This site has no content. "
                "It's a endpoint for sysmon reports.</p>")
