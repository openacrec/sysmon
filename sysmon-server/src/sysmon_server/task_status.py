from json import load

from sysmon_server import DATA_STORAGE


class TaskStatus:
    def __init__(self):
        with open(f"{DATA_STORAGE}/execution_status.json", "r") as in_file:
            self.json = load(in_file)

    @property
    def name(self):
        return self.json["name"]

    @property
    def command(self):
        return self.json["command"]

    @property
    def status(self):
        status = self.json["status"]
        if status == -1:
            return "Copying files over."
        if status == -2:
            return "Installing requirements."
        if status == -3:
            return "Running the task."
        if status == 1:
            return "Task failed!"
        if status == 0:
            return "Task finished!"
        if status is None:
            return "Unknown status."

    @property
    def clients(self):
        return self.json["clients"]
