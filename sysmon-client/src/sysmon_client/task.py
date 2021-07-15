"""
Define and handle definition of a Task
"""

import sys
from pathlib import Path
from typing import List

import spur

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
            use_stdout: bool = True):
        """
        Run a python file on all added remotes.

        :param filepath: Remote path of the python file to execute.
        :param args: Additional command line arguments.
        :param python_version: Specify the python version to use.
        :param use_stdout: If you want to print results to stdout.

        :return:
        """
        # TODO: See if you can test if the python version is available
        command = [f"python{python_version}", filepath]
        if args:
            command.extend(args)

        if use_stdout:
            stdout = sys.stdout
        else:
            stdout = None

        for remote in self.remotes:
            ssh = spur.SshShell(hostname=remote.hostname,
                                username=remote.username,
                                password=remote.password,
                                private_key_file=remote.key_file,
                                port=remote.port)
            with ssh:
                self.status = TaskStatus.RUNNING
                re = ssh.run(command, stdout=stdout, encoding="utf-8")

                self.output.append(re.output)
        self.status = TaskStatus.FINISHED
