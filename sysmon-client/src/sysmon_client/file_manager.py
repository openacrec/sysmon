from pathlib import Path
from typing import List

import spur

from .remote import Remote


class FileManager:
    def __init__(self,
                 source: str,
                 destination: str,
                 remotes: List[Remote],
                 auto_split: bool = False):

        self.source = Path(source).expanduser().resolve()
        if not self.source.exists():
            raise FileNotFoundError(self.source)

        self.destination = Path(destination)
        # if not self.destination.exists():
        #     # Need a way to check on remote
        #     raise FileNotFoundError(self.destination)

        self.remotes = remotes
        self.auto_split = auto_split

        self.splitted: List[List[Path]] = []

        self.files = []
        if self.source.is_dir():
            self.get_files(self.source)
        elif self.source.is_file():
            self.files.append(self.source)

        if self.auto_split:
            # Prepare a list where each sublist goes to another remote
            for _ in self.remotes:
                self.splitted.append([])
            self.split_files_up()
        else:
            self.splitted = [self.files]

    def get_files(self, folder: Path):
        for file in folder.iterdir():
            if file.is_file():
                self.files.append(file)
            elif file.is_dir():
                self.get_files(file)

    def split_files_up(self):
        for i, item in enumerate(self.files):
            if item.is_file():
                self.splitted[i % len(self.remotes)].append(item)

    def copy_to_remote(self):
        """
        Copy files to the remote using scp.

        :return:
        """
        with spur.LocalShell() as shell:
            for remote in self.remotes:
                shell.run([
                    "scp", "-r",
                    self.source,
                    f"{remote.username}@{remote.hostname}:{self.destination}"
                ])
        # TODO: Add better error if no directory there
        # TODO: If copying a directory, maybe create it using sth like:
        # $ scp -pr /source/directory user@host:the/target/directory
