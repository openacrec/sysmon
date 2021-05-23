import json
import socket
import time
from os import makedirs, environ

import hydra
import nvgpu
import psutil

system_stats = {"gpu": [], "cpu": [], "memory": [], "sensor": [], "disk": []}
machine_name = socket.gethostname() or environ["HOST"]


def update():
    """
    Collect and update the system_stats.

    :return:
    """
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    system_stats["cpu"].append([time_str, psutil.cpu_percent()])  # this gives an average
    system_stats["memory"].append(psutil.virtual_memory().percent)
    system_stats["gpu"].append(nvgpu.gpu_info())
    # system_stats["sensor"].append(psutil.sensors_temperatures())
    # system_stats["disk"].append(psutil.disk_partitions())


def generate_json(data_items):
    """
    Generates a json containing the set amount of data_items and saves them into a file.

    :param data_items: The amount of data points exported. Change in config/config.yaml.
    :return:
    """
    filtered_stats = {}
    for key in system_stats.keys():
        # Keep only the relevant history in memory
        system_stats[key] = system_stats[key][-data_items:]
        filtered_stats[key] = system_stats[key]

    output_dir_path = f"{hydra.utils.get_original_cwd()}/images/"
    makedirs(output_dir_path, exist_ok=True)
    with open(f"{output_dir_path}/{machine_name}.json", "w") as out:
        json.dump(filtered_stats, out)


@hydra.main(config_path="config/", config_name="config")
def sysmon_app(cfg):
    """
    Main function. Iterates every set amount of seconds to update the resource metrics.

    :param cfg: Config file. Gets passed through by @hydra decorator
    :return:
    """
    print(cfg)
    while True:
        update()
        # generate_graphs()
        generate_json(cfg.data_items)
        time.sleep(cfg.update_interval_in_s)


if __name__ == "__main__":
    sysmon_app()
