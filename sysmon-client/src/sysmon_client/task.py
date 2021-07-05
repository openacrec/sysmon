"""
Define and handle definition of a Task
"""

from typing import List
from task_status import TaskStatus


class Task:
    def __init__(self):
        self.task_name = ""
        self.number_of_machines = 0
        self.file_paths = []
        # List of individual statuses or one common for all remote tasks?
        self.status = TaskStatus.UNKNOWN

    def publish_running_task(self):
        # Probably separating notify logic to submodule
        # Probably internal method, called when starting the task
        raise NotImplementedError

    def execute_on_machines(self, number: int):
        # Look for (number of) machines that are "free" and save them to
        # establish remote connection later on
        # Will come at a far later stage, first just copying files
        raise NotImplementedError

    def copy_to_remote(self, file_paths: List):
        # TODO: Make this fill the list, not execute as if list was complete!
        # Probably as for publish_running_tasks, execute when task starts

        # Copy files to remote machines
        # If told, separate into "equal" chunks of data
        # "equal" as in number of folders or number of files
        # Possible structure, a sublist for each remote machine

        # Probably separate this logic and put it into a submodule
        self.file_paths = file_paths
        raise NotImplementedError
