from json import dump, load

from flask import request

from sysmon_server import DATA_STORAGE, MACHINE_NAMES_FILE


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

            with open(f"{DATA_STORAGE}/{req['machine_name']}.json", "w+") as out:
                dump(req, out)

            with open(MACHINE_NAMES_FILE, "r") as names_file:
                names_json = load(names_file)

                update_clients_and_times(req, names_json)

                with open(MACHINE_NAMES_FILE, "w") as out_names_file:
                    dump(names_json, out_names_file)
            return "Received!", 200
        else:
            return "Request was not JSON", 400
    else:
        return ("<p>This site has no content. "
                "It's a endpoint for sysmon reports.</p>")
