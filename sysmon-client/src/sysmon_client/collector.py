import time

import nvgpu
import psutil


class Collector:
    def __init__(self, name, interval):
        self.json = {
            "name": name,
            "interval": interval,
            "endpoint_version": "v01",
            "time": self.collect_time_string(),
            "timestamp": self.collect_time(),
            "cpu": self.collect_cpu(),
            "memory": self.collect_memory(),
            "gpu": self.collect_gpu_mem()
        }

    @staticmethod
    def collect_time() -> float:
        """Collect current time as unix timestamp."""
        return time.time()

    @staticmethod
    def collect_time_string() -> str:
        """Return the time from collect_time() as string"""
        timestamp = Collector.collect_time()
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

    @staticmethod
    def collect_cpu() -> float:
        """Collect current CPU workload."""
        return psutil.cpu_percent()

    @staticmethod
    def collect_memory() -> float:
        """Collect how much memory percent is used."""
        return psutil.virtual_memory().percent

    @staticmethod
    def collect_gpu_mem() -> float or None:
        """Collect how much memory is used on the GPU."""
        try:
            gpu_mem = nvgpu.gpu_info()[0]["mem_used_percent"]
        except FileNotFoundError:
            gpu_mem = None
            print("Couldn't find a GPU. Do you have a Nvidia GPU and drivers?")
            print("If you're using Docker, be sure to use the nvidia runtime.")
            print("If you don't have one, you can just ignore this message.")
        return gpu_mem
