"""
Module of main functions that make up sysmon
"""
import time

import collector
import submitter


def start_reporting(name: str, server_address: str, interval: int = 60):
    """
    Report's continuously the status of this machine to the sysmon_server.

    :param name: The name of this client, that will be displayed on the server
    :param server_address: Address, with endpoint, of the sysmon_server
    :param interval: Number of seconds between updates
    :return:
    """
    while True:

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

        submitter.continues_submit(system_stats, server_address)
        time.sleep(interval)


if __name__ == "__main__":
    # start_reporting("Test", "http://127.0.0.1:5000", 5)
    submitter.request_deletion({"name": "NoGpu"}, "http://127.0.0.1:5000")
