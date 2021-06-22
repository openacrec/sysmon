import json
import time
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


# TODO: Actually use and update the lists, currently only the last entry is
#  present.
#  Properly load from disk at some point to check/get old data.
class Client:
    """Data class that wraps Client information."""

    def __init__(self, client_json: Dict):
        self.json = client_json

    @property
    def name(self) -> str:
        return self.json["name"]

    @property
    def interval(self) -> int:
        return self.json["interval"]

    @property
    def endpoint_version(self) -> str:
        return self.json["endpoint_version"]

    @property
    def time(self) -> str:
        return self.json["time"]

    @property
    def timestamp(self) -> float:
        return self.json["timestamp"]

    @property
    def cpu(self) -> List:
        return self.json["cpu"]

    @cpu.setter
    def cpu(self, new_cpu: float):
        if self.cpu:
            self.json["cpu"].append(new_cpu)

    @property
    def memory(self) -> List:
        return self.json["memory"]

    @memory.setter
    def memory(self, new_memory: float):
        if self.cpu:
            self.json["memory"].append(new_memory)

    @property
    def gpu(self) -> List:
        return self.json["gpu"]

    @gpu.setter
    def gpu(self, new_gpu: float):
        if self.cpu:
            self.json["gpu"].append(new_gpu)

    def save_file(self):
        filename = secure_filename(self.name)
        with open(f"{DATA_STORAGE}/{filename}.json", "w+") as out:
            json.dump(self.json, out)

    def updated_in_time(self) -> bool:
        current_time = time.time()
        # Give 10 seconds as extra delay
        if current_time > self.timestamp + self.interval + 10:
            return False
        else:
            return True
