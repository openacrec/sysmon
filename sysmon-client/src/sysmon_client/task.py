"""
Define and handle definition of a Task
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Union

from .file_manager import FileManager
from .remote import Remote
from .task_status import TaskStatus
from .notify import Notify


class Task:
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.remotes: List[Remote] = []
        self.output = []
        self.notify: Notify = Notify("", task_name)
        self.publish: bool = False

    def add_remote(self,
                   name: str,
                   url: str,
                   username: str,
                   password: str = None,
                   key_file: str or Path = None,
                   port: int = 22,
                   do_connection_test: bool = True,
                   create_target: bool = False):
        """
        Create a Remote object, that handles connecting and execution of command
        on the specified remote.

        :param name: Specify athe name for this remote. Needed to display status
        on server on the correct spot. Does not affect is status is send.
        :param url: The address to connect via ssh to the remote.
        :param username: The username to login to the remote.
        :param password: The password used to login to the remote.
        :param key_file: The path to the keyfile to authenticate if you prefer it.
        :param port: Specify a different port to use for a ssh connection (default: 22)
        :param do_connection_test: Whether to try connection once when the Remote
        object is created.
        :param create_target: Whether or not to create the first folder on the remote
        if it does not exist
        :return:
        """
        re = Remote(name,
                    url,
                    username,
                    password,
                    key_file,
                    port,
                    do_connection_test,
                    create_target)
        if re not in self.remotes:
            self.remotes.append(re)

    def publish_task_on(self, sysmon_address: str):
        """
        If called the sysmon tries to send information about the tasks status to the
        sysmon server.

        :param sysmon_address: The address of the sysmon server.
        :return:
        """
        self.publish = True
        self.notify = Notify(sysmon_address, self.task_name)

    def copy(self, source: str, destination: str, auto_split: bool = False):
        """
        Copy to every specified remote when task is started.

        :param source: path to file/folder
        :param destination: remote path, relative to home (~, default) or root (/)
        :param auto_split: Split folders into equal chunks
        :return:
        """
        self.notify.remotes = self.remotes
        self.notify.task_command = f"scp -r {source} {destination}"
        self.notify.status = TaskStatus.COPYING
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
        # TODO: Output format: Should contain machine, timestamp and message

        command = [f"python{python_version}", filepath]
        if args:
            command.extend(args)
        # TODO: Move Notify to remote, so that each remote has its own status
        self.notify.remotes = self.remotes
        self.notify.task_command = " ".join(command)
        self.notify.status = TaskStatus.RUNNING
        with ThreadPoolExecutor(max_workers=len(self.remotes)) as executor:
            future_output = [executor.submit(remote.execute, command, use_stdout)
                             for remote in self.remotes]
            for output in as_completed(future_output):
                self.output.append(output.result())
        self.notify.status = TaskStatus.FINISHED

    def install_req(self, req: Union[str, Path, List[str]], python_version: float = 3):
        """
        Install python requirements for code execution using pip.

        :param req: Accepts a filepath, as string or Path. One module per line.
        You can also name the package. One as string, multiple as list of strings.
        :param python_version: The python version to use when calling pip.
        :return:
        """
        # Find out what the input was
        try:
            file = Path(req)
        except TypeError:
            # If its a list of packages
            packages = req
        else:
            if file.exists():
                if file.is_file():
                    with open(file, "r") as in_file:
                        packages = [package for package in in_file]
            else:
                # If the input was a single string, but not a file
                if type(req) == str:
                    # Filter out paths, that didn't exist
                    packages = [req]

        # The packages always get input as a list, ordered, in case a file was given,
        # the order is from top to bottom
        command = [f"python{python_version}", "-m", "pip", "install"]
        command.extend(packages)
        self.notify.remotes = self.remotes
        self.notify.task_command = " ".join(command[0:6]) + " ..."
        self.notify.status = TaskStatus.INSTALLING
        with ThreadPoolExecutor(max_workers=len(self.remotes)) as executor:
            [executor.submit(remote.execute, command, False)
             for remote in self.remotes]
