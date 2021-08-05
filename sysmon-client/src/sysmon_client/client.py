import time

from .collector import Collector
from .submitter import continues_submit


class Client:
    """Defines a client that reports usage statistics to a specified server."""

    def __init__(self, name: str, server_address: str, report_interval: int = 60):
        """
        Initialize the Client class.

        :param name: Name of this client, that will be displayed on the server.
        :param server_address: Address of the sysmon_server.
        :param report_interval: Number of seconds between sending a report.
        """
        self.name = name
        self.server_address = server_address
        self.report_interval = report_interval

    def start_reporting(self):
        """Report's continuously the status of this machine to the sysmon_server."""
        while True:
            system_stats = Collector(self.name, self.report_interval)
            continues_submit(system_stats.json, self.server_address)
            time.sleep(self.report_interval)


def entry_point_helper():
    """Helper function to query necessary information when the entrypoint
    "sysmon-report" is used."""
    name = input("How do you want to call this client? ")
    server_address = input("Which address does the sysmon_server have? ")
    return Client(name, server_address).start_reporting()


if __name__ == "__main__":
    Client("Test", "http://127.0.0.1:5000", 5).start_reporting()
    # submitter.request_deletion({"name": "NoGpu"}, "http://127.0.0.1:5000")
