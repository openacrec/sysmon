"""
Module of main functions that make up sysmon
"""

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

    while True:
        submitter.continues_submit(system_stats, server_address)


if __name__ == "__main__":
    start_reporting("Test", "http://localhost:5000/v01/")
