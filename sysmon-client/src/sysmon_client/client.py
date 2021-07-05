"""
Module of main functions that make up sysmon
"""
import time

from collector import Collector
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
        system_stats = Collector(name, interval)
        submitter.continues_submit(system_stats.json, server_address)
        time.sleep(interval)


if __name__ == "__main__":
    start_reporting("Test", "http://127.0.0.1:5000", 5)
    # submitter.request_deletion({"name": "NoGpu"}, "http://127.0.0.1:5000")
