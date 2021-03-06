import math
import sys
import warnings
from pathlib import Path
from typing import List

import spur


class Remote:
    """Establish remote connection and issue commands over ssh."""

    def __init__(self,
                 name: str,
                 url: str,
                 username: str,
                 password: str = None,
                 key_file: str or Path = None,
                 port: int = 22,
                 do_connection_test: bool = True,
                 create_target: bool = False):
        """
        Initialize the Remote class.

        :param name: Name of this remote (should be as displayed be sysmon_server for
        identification).
        :param url: URL of this remote server (as you would use for ssh).
        :param username: Username to log into with on this server.
        :param password: Password for this user (optional).
        :param key_file: Path to a key_file for this user (optional).
        :param port: Change the used port (optional).
        :param do_connection_test: Whether or not to test the connection immediately.
        :param create_target: Whether or not the target folder should be created if its
        missing.
        """

        # Name as displayed in sysmon server
        self.name = name
        self.url = url
        self.username = username
        self.password = password
        if key_file:
            key_file = Path(key_file).expanduser().resolve()
            if key_file.is_file():
                # Spur does not work with Path input
                self.key_file = str(key_file)
            else:
                raise FileNotFoundError(f"No keyfile found: {key_file}")
        else:
            # This way an input of "" is going back to None
            # Default of spur for no key is None
            self.key_file = None
        self.port = port
        self.create_target = create_target

        if do_connection_test:
            self.test_connection()

    def get_ssh_shell(self):
        """Return a ssh shell to use for remote execution of a command."""
        return spur.SshShell(hostname=self.url,
                             username=self.username,
                             password=self.password,
                             private_key_file=self.key_file,
                             port=self.port)

    def test_connection(self):
        """Run simple test command, errors out if authentication fails."""
        shell = self.get_ssh_shell()
        with shell:
            shell.run(["pwd"])
            print(f"Connection with remote {self.url} successfully established.")

    def test_python_version(self, version: float):
        """Test if the desired python version is on the remote."""
        # Since casting to float makes int x -> x.0
        if version == 2.0:
            return 2
        if version == 3.0:
            return 3
        command = [f"python{version}"]
        shell = self.get_ssh_shell()
        with shell:
            try:
                shell.run(command, encoding="utf-8")
            except spur.errors.NoSuchCommandError:
                fallback = math.floor(version)
                warnings.warn(f"Could not find python {version} on {self.url}."
                              f"Trying broader python{fallback} command.")
                return fallback
            else:
                return version

    def execute(self, command: List[str], use_stdout: bool):
        """
        Execute commands on all registered remotes.

        :param command: The command to execute.
        :param use_stdout: Whether the output should go to your stdout.
        :return:
        """
        if use_stdout:
            stdout = sys.stdout
        else:
            stdout = None

        if command[0].startswith("python"):
            # Once support moves to 3.9+ only, you can use, which is more readable:
            # self.test_python_version(float(command[0].removeprefix("python")))
            version = self.test_python_version(float(command[0][6:]))
            command[0] = f"python{version}"
        shell = self.get_ssh_shell()
        with shell:
            re = shell.run(command, stdout=stdout, encoding="utf-8")
        return re.output

    def __eq__(self, other: "Remote"):
        """Assume a remote to be the same if these conditions are met."""
        hostnames = self.url == other.url
        usernames = self.username == other.username
        ports = self.port == other.port
        return hostnames and usernames and ports
