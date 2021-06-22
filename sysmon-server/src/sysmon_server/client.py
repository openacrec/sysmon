import json
import pathlib
import time
from json import load
from typing import Dict, List

from werkzeug.utils import secure_filename

from sysmon_server import DATA_STORAGE

"""v01 json format:
system_stats = {
        "name": name,
        "interval": interval,
        "endpoint_version": "v01",
        "time": collector.collect_time_string(),
        "timestamp": collector.collect_time(),
        "cpu": collector.collect_cpu(),
        "memory": collector.collect_memory(),
        "gpu": collector.collect_gpu_mem()
    }
"""


# TODO: Limit list length
class Client:
    """Data class that wraps Client information."""

    def __init__(self, client_json: Dict, limited: bool = False):
        """
        Create a new client object.

        :param client_json: client json provided by api endpoints
        :param limited: if True, client only knows the client name
        """
        # Try to load existing client data
        try:
            filename = secure_filename(client_json["name"])
            with open(f"{DATA_STORAGE}/{filename}.json", "r") as in_file:
                self.json = load(in_file)
        except FileNotFoundError:
            # New clients here, no file for them yet
            client_json["cpu"] = [client_json["cpu"]]
            client_json["memory"] = [client_json["memory"]]
            client_json["gpu"] = [client_json["gpu"]]
            self.json = client_json
        else:
            if not limited:
                # If it was an old client, update it's attributes
                self.update_all(client_json)

    def update_all(self, json_data):
        self.interval = json_data["interval"]
        self.endpoint_version = json_data["endpoint_version"]
        self.time = json_data["time"]
        self.timestamp = json_data["timestamp"]
        self.cpu = json_data["cpu"]
        self.memory = json_data["memory"]
        self.gpu = json_data["gpu"]

    @property
    def name(self) -> str:
        return self.json["name"]

    @property
    def interval(self) -> int:
        return self.json["interval"]

    @interval.setter
    def interval(self, new_interval):
        self.json["interval"] = new_interval

    @property
    def endpoint_version(self) -> str:
        return self.json["endpoint_version"]

    @endpoint_version.setter
    def endpoint_version(self, new_endpoint_version):
        self.json["endpoint_version"] = new_endpoint_version

    @property
    def time(self) -> str:
        return self.json["time"]

    @time.setter
    def time(self, new_time):
        self.json["time"] = new_time

    @property
    def timestamp(self) -> float:
        return self.json["timestamp"]

    @timestamp.setter
    def timestamp(self, new_timestamp):
        self.json["timestamp"] = new_timestamp

    @property
    def cpu(self) -> List:
        return self.json["cpu"]

    @cpu.setter
    def cpu(self, new_cpu: float):
        if self.cpu:
            self.json["cpu"].append(new_cpu)
        else:
            self.json["cpu"] = [new_cpu]

    @property
    def memory(self) -> List:
        return self.json["memory"]

    @memory.setter
    def memory(self, new_memory: float):
        if self.memory:
            self.json["memory"].append(new_memory)
        else:
            self.json["memory"] = [new_memory]

    @property
    def gpu(self) -> List:
        return self.json["gpu"]

    @gpu.setter
    def gpu(self, new_gpu: float):
        if self.gpu:
            self.json["gpu"].append(new_gpu)
        else:
            self.json["gpu"] = [new_gpu]

    @staticmethod
    def update_statistics(client, json_data):
        print("working in update")
        print(json_data)

        return client

    def save_file(self):
        filename = secure_filename(self.name)
        with open(f"{DATA_STORAGE}/{filename}.json", "w+") as out:
            json.dump(self.json, out)

    def updated_in_time(self) -> bool:
        current_time = time.time()
        # Give 10 seconds as extra delay
        if current_time > self.timestamp + self.interval + 10:
            return False
        # Checks if client is offline for more than 3 days
        elif current_time > self.timestamp + (86400 * 3):
            self.delete_file()
            return False
        else:
            return True

    def delete_file(self):
        filename = secure_filename(self.name)
        try:
            pathlib.Path(f"{DATA_STORAGE}/{filename}.json").unlink()
        except FileNotFoundError:
            print("Could not find client data to delete.")
