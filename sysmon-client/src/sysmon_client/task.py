"""
Define and handle definition of a Task
"""

from pathlib import Path

from .file_manager import FileManager
from .remote import Remote
from .task_status import TaskStatus


# TODO: Contemplate a server module, that handles requesting for free remotes
# This should return remote name and address? Or not?


class Task:
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.number_of_machines = 0
        self.status = TaskStatus.UNKNOWN
        self.remotes = []

    def add_remote(self,
                   hostname: str,
                   username: str,
                   password: str = None,
                   key_file: str or Path = None,
                   port: int = 22):
        re = Remote(hostname, username, password, key_file, port)
        if re not in self.remotes:
            self.remotes.append(re)

    def publish_running_task(self):
        # Probably separating notify logic to submodule
        # Probably internal method, called when starting the task
        raise NotImplementedError

    def execute_on_machines(self, number: int):
        # Look for (number of) machines that are "free" and save them to
        # establish remote connection later on
        # Will come at a far later stage, first just copying files
        raise NotImplementedError

    def copy(self,
             source: str,
             destination: str,
             auto_split: bool = False):
        """
        Copy to every specified remote when task is started.

        :param source: path to file/folder
        :param destination: remote path, relative to home (~, default) or root (/)
        :param auto_split: Split folders into equal chunks
        :return:
        """
        # Copy files to remote machines
        # If told, separate into "equal" chunks of data
        # "equal" as in number of folders or number of files
        # Possible structure, a sublist for each remote machine

        # Probably separate this logic and put it into a submodule
        files = FileManager(source,
                            destination,
                            self.remotes,
                            auto_split)
        files.copy_to_remote()
