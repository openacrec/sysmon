from json import dump, load
from os import path

from flask import Flask, request, render_template

app = Flask(__name__)

MACHINE_NAMES_FILE = f"{app.root_path}/static/machine_names.json"
NAMES_JSON = {"names": [], "times": []}


# If you already have a list of known machines, keep it contents
if path.isfile(MACHINE_NAMES_FILE):
    with open(MACHINE_NAMES_FILE, "r") as in_file:
        NAMES_JSON = load(in_file)
with open(MACHINE_NAMES_FILE, "w+") as out_file:
    dump(NAMES_JSON, out_file)


@app.route("/")
def sysmon():
    """
    Reads all machine names in and returns a page with a list of those.

    :return:
    """
    with open(MACHINE_NAMES_FILE, "r") as names_file:
        machine_names = load(names_file)
        known_names = machine_names["names"]
    return render_template("index.html", hosts=known_names)


def update_clients_and_times(req, names_json):
    """
    New clients should go straight into the names list,
    while old clients get there "last seen" time updated.

    :param req: the json with the new client info
    :param names_json: the json with the list of names and "last seen" times
    :return:
    """
    new_name = req["machine_name"]
    new_time = req["time"][-1]
    machine_names = names_json["names"]
    machine_times = names_json["times"]

    if new_name not in machine_names:
        machine_names.append(new_name)
        machine_times.append(new_time)
    else:
        new_times = []
        for name, time in zip(machine_names, machine_times):
            if name == new_name:
                new_times.append(new_time)
            else:
                new_times.append(time)
    names_json["names"] = machine_names
    names_json["times"] = machine_times
    return names_json


@app.route("/post", methods=['GET', 'POST'])
def json_handler():
    """
    Handles incoming json data. Save's each json into a file. Separately saves
    the machines names to handle the template for new, unknown hosts.

    :return:
    """
    if request.method == 'POST':
        if request.is_json:
            req = request.get_json()

            static_dir = f"{app.root_path}/static"
            with open(f"{static_dir}/{req['machine_name']}.json", "w+") as out:
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
        return "<p>This site has no content. " \
               "It's a endpoint for sysmon reports.</p>"


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
