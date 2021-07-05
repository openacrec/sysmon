from typing import List
from pathlib import Path


class DataManager:
    def __init__(self, number_of_servers: int, file_paths: List):
        # Make this true for sub folders by default?
        self.create_folders = False

        self.number_of_servers = number_of_servers
        # Use pathlib, to make it easier to check file type and maybe path
        # manipulation, does this need a check that no Paths are already there?
        # First test says: no need to care
        self.file_paths = [Path(file_path) for file_path in file_paths]

    def split_files_up(self):
        # If needed split files or folders by the number of clients used
        pass

    def copy_files_to_servers(self):
        # Probably getting Remote object, that will actually handle logic
        # Need to see, if we need a self.server(s) for that, then no need for
        # separate number of servers input
        pass
