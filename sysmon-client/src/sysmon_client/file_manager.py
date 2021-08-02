from pathlib import Path
from typing import List

import spur

from .remote import Remote


class FileManager:
    """Helper class that handles file path handling as well as splitting of data."""

    def __init__(self,
                 source: str,
                 destination: str,
                 remotes: List[Remote],
                 auto_split: bool = False):
        """
        Initialize the FileManager class.

        :param source: Source path of the file/folder to copy.
        :param destination: Path of the destination on the remote.
        :param remotes: List of the remotes where this will be copied to.
        :param auto_split: Whether this is a folder which content shall be split
        between the remotes.
        """

        self.remotes = remotes

        self.source = Path(source).expanduser().resolve()
        if not self.source.exists():
            raise FileNotFoundError(self.source)
        self.destination = Path(destination)
        self.check_path_on_remotes_exists()

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
        """Collect all files in this folder, including sub folders."""
        for file in folder.iterdir():
            if file.is_file():
                self.files.append(file)
            elif file.is_dir():
                self.get_files(file)

    def split_files_up(self):
        """Split all collected files up into equal groups."""
        for i, item in enumerate(self.files):
            if item.is_file():
                self.splitted[i % len(self.remotes)].append(item)

    def check_path_on_remotes_exists(self):
        """Check whether a (folder) path is accessible on the remote."""
        path = self.destination.parent
        for remote in self.remotes:
            command = ["stat", str(path)]
            try:
                remote.execute(command, False)
            except spur.results.RunProcessError:
                if remote.create_target:
                    self.create_parent_folders()
                else:
                    raise FileNotFoundError(self.destination)

    def create_parent_folders(self):
        """Calls for the creation of the destinations parent folder on all remotes.
        Subfolders are created anyways by the used copy function."""
        path = self.destination.parent
        if not path == ".":
            for remote in self.remotes:
                command = ["mkdir", "-p", str(path)]
                remote.execute(command, use_stdout=False)

    def copy_to_remote(self):
        """Copy files to the remote using scp."""
        with spur.LocalShell() as shell:
            for remote in self.remotes:
                shell.run([
                    "scp", "-r",
                    self.source,
                    f"{remote.username}@{remote.url}:{self.destination}"
                ])
