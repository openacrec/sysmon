import warnings
from json import dump, load
from os import path
from time import strftime, strptime, localtime, mktime

from flask import render_template

from sysmon_server import app, DATA_STORAGE, MACHINE_NAMES_FILE
from .endpoints import legacy

NAMES_JSON = {"names": [], "times": []}

# If you already have a list of known machines, keep it contents
if path.isfile(MACHINE_NAMES_FILE):
    with open(MACHINE_NAMES_FILE, "r") as in_file:
        NAMES_JSON = load(in_file)
with open(MACHINE_NAMES_FILE, "w+") as out_file:
    dump(NAMES_JSON, out_file)


def try_strptime(time_string, time_format):
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


def check_update_timings_legacy(names, times):
    """
    Checks if there is a host that did not update in time.
    Default interval if no interval is specified is one day.

    Only for legacy purpose. Deprecated.

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
        with open(f"{DATA_STORAGE}/{name}.json") as host_file:
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
    Render a site showing status of all connected clients.

    :return:
    """
    with open(MACHINE_NAMES_FILE, "r") as names_file:
        machine_names = load(names_file)
        known_names = machine_names["names"]
        known_times = machine_names["times"]
        alive, disconnected = check_update_timings_legacy(known_names,
                                                          known_times)
    return render_template("index.html",
                           hosts=known_names,
                           alive=alive,
                           disconnected=disconnected)


def check_compatible_endpoint_version():
    raise NotImplementedError


@app.route("/post", methods=['GET', 'POST'])
def legacy_endpoint():
    """
    Handles incoming json data. Save's each json into a file. Separately saves
    the machines names to handle the template for new, unknown hosts.

    :return:
    """
    warnings.warn("Legacy endpoint.", DeprecationWarning)
    return legacy.json_handler()


@app.route("/api/v01", methods=['POST'])
def v01_endpoint():
    """

    :return:
    """
    pass


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
