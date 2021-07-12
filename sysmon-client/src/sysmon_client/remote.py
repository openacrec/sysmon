"""
Establish remote connection and issue commands over ssh
"""
from pathlib import Path
from typing import List
import spur


# TODO: Evaluate if i can provide an easier interface for our use cases
# Otherwise integrate spur into the functions that would call this
# One immediate pro: Can save this for use throughout, no need to provide
# login information multiple times (in code)


class Remote:
    def __init__(self,
                 hostname: str,
                 username: str,
                 password: str = None,
                 key_file: str or Path = None,
                 port: int = 22):
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

        # Enables arbitrary execution on remote.
        self.local_shell = spur.LocalShell()
        self.shell = spur.SshShell(hostname=self.hostname,
                                   username=self.username,
                                   password=self.password,
                                   private_key_file=self.key_file,
                                   port=self.port)

        self.test_connection()

    def test_connection(self):
        """Run simple test command, errors out if authentication fails."""
        with self.shell as shell:
            shell.run(["pwd"])


if __name__ == '__main__':
    pass
