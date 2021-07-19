"""
Establish remote connection and issue commands over ssh
"""
import sys
from pathlib import Path
from typing import List

import spur


# TODO: Evaluate if i can provide an easier interface for our use cases
# Otherwise integrate spur into the functions that would call this
# One immediate pro: Can save this for use throughout, no need to provide
# login information multiple times (in code)


# TODO: Match/Identify with what is what on server side


class Remote:
    def __init__(self,
                 hostname: str,
                 username: str,
                 password: str = None,
                 key_file: str or Path = None,
                 port: int = 22,
                 do_connection_test: bool = True,
                 create_target: bool = False):
        self.hostname = hostname
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
        return spur.SshShell(hostname=self.hostname,
                             username=self.username,
                             password=self.password,
                             private_key_file=self.key_file,
                             port=self.port)

    def test_connection(self):
        """Run simple test command, errors out if authentication fails."""
        shell = self.get_ssh_shell()
        with shell:
            shell.run(["pwd"])
            print(f"Connection with remote {self.hostname} successfully established.")

    def execute(self, command: List[str], use_stdout: bool):
        if use_stdout:
            stdout = sys.stdout
        else:
            stdout = None
        shell = self.get_ssh_shell()
        with shell:
            re = shell.run(command, stdout=stdout, encoding="utf-8")
        return re.output

    def __eq__(self, other):
        """Assume a remote to be the same if these conditions are met."""
        hostnames = self.hostname == other.hostname
        usernames = self.username == other.username
        ports = self.port == other.port
        return hostnames and usernames and ports


if __name__ == '__main__':
    pass
