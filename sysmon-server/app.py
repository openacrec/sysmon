from json import dump, load
from os import path
from time import strftime, strptime, localtime, mktime
from flask import Flask, request, render_template

app = Flask(__name__)

STATIC_DIR = f"{app.root_path}/static"
MACHINE_NAMES_FILE = f"{app.root_path}/static/machine_names.json"
NAMES_JSON = {"names": [], "times": []}

# If you already have a list of known machines, keep it contents
if path.isfile(MACHINE_NAMES_FILE):
    with open(MACHINE_NAMES_FILE, "r") as in_file:
        NAMES_JSON = load(in_file)
with open(MACHINE_NAMES_FILE, "w+") as out_file:
    dump(NAMES_JSON, out_file)


def try_strptime(time_string, time_format):
    """
    Ties to convert the time (given as string) to time epoch.

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


def check_update_timings(names, times):
    """
    Checks if there is a host that did not update in time.
    Default interval if no interval is specified is one day.

    :param names: A list of all host names
    :param times: A list of corresponding time stamps from the latest update
    :return: A tuple of alive and disconnected host names
    """
    alive = []
    disconnected = []
    time_format = "%Y-%m-%d %H:%M:%S"
    current_time = strftime(time_format, localtime())
    current_time = try_strptime(current_time, time_format)

    for name, time in zip(names, times):
        last_time = try_strptime(time, time_format)
        with open(f"{STATIC_DIR}/{name}.json") as host_file:
            # Until all clients give an interval, we need to catch a KeyError
            try:
                interval = load(host_file)["interval"]
            except KeyError:
                # Since we don't have the actual interval time
                # Assume it posts once a day.
                interval = 86400
        # Add a little to the interval to filter cases where the
        # processing or sending took a few seconds, but it's still alive
        if current_time - last_time < interval + 30:
            alive.append(name)
        else:
            disconnected.append(name)
    return alive, disconnected


@app.route("/")
def sysmon():
    """
    Reads all machine names in and returns a page with a list of those.

    :return:
    """
    with open(MACHINE_NAMES_FILE, "r") as names_file:
        machine_names = load(names_file)
        known_names = machine_names["names"]
        known_times = machine_names["times"]
        alive, disconnected = check_update_timings(known_names, known_times)
    return render_template("index.html",
                           hosts=known_names,
                           alive=alive,
                           disconnected=disconnected)


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

            with open(f"{STATIC_DIR}/{req['machine_name']}.json", "w+") as out:
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
