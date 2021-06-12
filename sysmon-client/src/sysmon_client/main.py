import json
import time
from http import HTTPStatus
from os import makedirs

import hydra
import nvgpu
import psutil
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

GPU_EXISTS = True


def update(system_stats):
    """
    Collect and update the system_stats.

    :return:
    """
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    system_stats["time"].append(time_str)
    system_stats["cpu"].append(psutil.cpu_percent())
    system_stats["memory"].append(psutil.virtual_memory().percent)
    global GPU_EXISTS
    if GPU_EXISTS:
        try:
            system_stats["gpu"].append(nvgpu.gpu_info()[0]["mem_used_percent"])
        except FileNotFoundError:
            GPU_EXISTS = False
            del system_stats["gpu"]
            print("No nvidia-smi found. Do you have a Nvidia GPU and Drivers?")
            print("If you're using Docker, be sure to use the nvidia runtime.")
            print("If you don't have one, you can ignore this message.")
    return system_stats


def relevant_data(system_stats, number_of_data_items):
    """
    Discard data, that does not fit into the number_of_data_items.

    :param system_stats: Current system statistics
    :param number_of_data_items: Number of items that are relevant
    :return: system_stats with still relevant data inside
    """
    for key in system_stats.keys():
        if isinstance(key, list):
            system_stats[key] = system_stats[key][-number_of_data_items:]
    return system_stats


def save_json_file(system_stats):
    """
    Generates a json containing the set amount of data_items and saves
    them into a file.

    :param system_stats: Current system statistics
    :return:
    """
    output_dir_path = f"{hydra.utils.get_original_cwd()}/images"
    makedirs(output_dir_path, exist_ok=True)
    filename = f"{system_stats['machine_name']}.json"
    with open(f"{output_dir_path}/{filename}", "w") as out:
        json.dump(system_stats, out)


def send_to_server(system_stats, server_address, client_name):
    """
    Send current system statistics to provided endpoint.

    :param system_stats: Current system statistics
    :param client_name: this clients name
    :param server_address: address of the server collecting system stats
    :return:
    :raises: requests.exceptions.ConnectionError
    """
    try:
        with requests.session() as session:
            session.mount("http://", HTTPAdapter(
                max_retries=Retry(total=5,
                                  connect=3,
                                  redirect=10,
                                  backoff_factor=0.5,
                                  status_forcelist=[
                                      HTTPStatus.REQUEST_TIMEOUT,
                                      # HTTP 408
                                      HTTPStatus.CONFLICT,
                                      # HTTP 409
                                      HTTPStatus.INTERNAL_SERVER_ERROR,
                                      # HTTP 500
                                      HTTPStatus.BAD_GATEWAY,
                                      # HTTP 502
                                      HTTPStatus.SERVICE_UNAVAILABLE,
                                      # HTTP 503
                                      HTTPStatus.GATEWAY_TIMEOUT
                                      # HTTP 504
                                  ])))

            re = session.post(server_address, json=system_stats)
            if re.status_code != 200:
                print(re.status_code, re.reason)
            else:
                print(f"[{system_stats['time'][-1]}] "
                      f"Updated system statistics on {client_name}.")
    except requests.exceptions.RequestException:
        print(f"[{system_stats['time'][-1]}] "
              f"Could not update system statistics on {client_name}.")


@hydra.main(config_path="config/", config_name="config")
def sysmon_app(cfg):
    """
    Main function. Iterates every set amount of seconds to update
    the resource metrics.

    :param cfg: Config file. Gets passed through by @hydra decorator
    :return:
    """
    system_stats = {"machine_name": cfg.client.name,
                    "interval": cfg.client.update_interval_in_s,
                    "time": [],
                    "cpu": [],
                    "memory": [],
                    "gpu": []}
    while True:
        system_stats = update(system_stats)
        system_stats = relevant_data(system_stats,
                                     cfg.client.number_of_data_items)
        save_json_file(system_stats)
        send_to_server(system_stats, cfg.server.address, cfg.client.name)
        time.sleep(cfg.client.update_interval_in_s)


if __name__ == "__main__":
    sysmon_app()
