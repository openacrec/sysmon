from typing import List

from .task_status import TaskStatus
from .remote import Remote
from .submitter import send_task_status


class Notify:
    """Handles reaction on status changes and reports them to the server."""

    def __init__(self, sysmon_address: str, task_name: str):
        """
        Initialize the Notify class.

        :param sysmon_address: Server address of the used sysmon_server instance.
        :param task_name: Name of the task this report talks about.
        """

        self.sysmon_address = sysmon_address
        self.task_name = task_name
        self.task_command = "Nothing yet-"
        self.remotes: List[Remote] = []
        self._status = TaskStatus.UNKNOWN

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status: TaskStatus):
        self._status = new_status
        self.notify()

    def notify(self):
        """Notify sysmon sever that a task is executing on a client."""
        status = {
            "name": self.task_name,
            "command": self.task_command,
            "status": self.status.value,
            "clients": [remote.name for remote in self.remotes]
        }
        send_task_status(status, self.sysmon_address)
