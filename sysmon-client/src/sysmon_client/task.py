"""
Define and handle definition of a Task
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List

from .file_manager import FileManager
from .remote import Remote
from .task_status import TaskStatus


# TODO: Contemplate a server module, that handles requesting for free remotes
# This should return remote name and address? Or not?


class Task:
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.status = TaskStatus.UNKNOWN
        self.remotes: List[Remote] = []
        self.output = []

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
        self.status = TaskStatus.COPYING
        files = FileManager(source,
                            destination,
                            self.remotes,
                            auto_split)
        files.copy_to_remote()

    def run(self, filepath: str,
            args: List[str] = None,
            python_version: float = 3,
            use_stdout: bool = False):
        """
        Run a python file on all added remotes.

        :param filepath: Remote path of the python file to execute.
        :param args: Additional command line arguments.
        :param python_version: Specify the python version to use.
        :param use_stdout: Whether you want to print results to stdout.

        :return:
        """
        # TODO: See if you can test if the python version is available
        # TODO: Output format: Should contain machine, timestamp and message

        command = [f"python{python_version}", filepath]
        if args:
            command.extend(args)

        self.status = TaskStatus.RUNNING
        with ThreadPoolExecutor(max_workers=len(self.remotes)) as executor:
            future_output = [executor.submit(remote.execute, command, use_stdout)
                             for remote in self.remotes]
            for output in as_completed(future_output):
                self.output.append(output.result())

        self.status = TaskStatus.FINISHED
