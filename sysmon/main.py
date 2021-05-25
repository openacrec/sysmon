import json
import time
from os import makedirs, environ

import requests.exceptions
from requests import post

import hydra
import nvgpu
import psutil


def update(system_stats):
    """
    Collect and update the system_stats.

    :return:
    """
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    system_stats["cpu"].append([time_str, psutil.cpu_percent()])  # this gives an average
    system_stats["memory"].append(psutil.virtual_memory().percent)
    system_stats["gpu"].append(nvgpu.gpu_info())
    return system_stats


def relevant_data(system_stats, number_of_data_items):
    """
    Discard data, that does not fit into the number_of_data_items.

    :param system_stats: Current system statistics
    :param number_of_data_items: Number of items that are relevant
    :return: system_stats with still relevant data inside
    """
    for key in system_stats.keys():
        # Keep only the relevant history in memory
        system_stats[key] = system_stats[key][-number_of_data_items:]
    return system_stats


def save_json_file(system_stats):
    """
    Generates a json containing the set amount of data_items and saves them into a file.

    :param system_stats: Current system statistics
    :return:
    """
    output_dir_path = f"{hydra.utils.get_original_cwd()}/images/"
    makedirs(output_dir_path, exist_ok=True)
    with open(f"{output_dir_path}/{system_stats['machine_name']}.json", "w") as out:
        json.dump(system_stats, out)


def send_to_server(system_stats):
    """
    Send current system statistics to provided endpoint.

    :param system_stats: Current system statistics
    :return:
    """
    json_endpoint = environ["JSON_ENDPOINT"]
    req = post(json_endpoint, json=system_stats)
    if req.status_code != 200:
        print(req.reason)
        raise requests.exceptions.RequestsWarning
    else:
        print(f"[{system_stats['cpu'][0][0]}] Updated system statistics on {environ['HOSTNAME']}.")


@hydra.main(config_path="config/", config_name="config")
def sysmon_app(cfg):
    """
    Main function. Iterates every set amount of seconds to update the resource metrics.

    :param cfg: Config file. Gets passed through by @hydra decorator
    :return:
    """
    system_stats = {"machine_name": environ["HOSTNAME"], "cpu": [], "memory": [], "gpu": []}
    while True:
        system_stats = update(system_stats)
        system_stats = relevant_data(system_stats, cfg.number_of_data_items)
        save_json_file(system_stats)
        send_to_server(system_stats)
        time.sleep(cfg.update_interval_in_s)


if __name__ == "__main__":
    sysmon_app()
