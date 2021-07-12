from pathlib import Path


class FileManager:
    def __init__(self,
                 source: str,
                 destination: str,
                 auto_split: int = 1,
                 create_dir: bool = False):
        self.source = Path(source).expanduser().resolve()
        if not self.source.exists():
            raise FileNotFoundError(self.source)
        self.destination = Path(destination).expanduser().resolve()
        # if not self.destination.exists():
        #     # Need a way to check on remote
        #     raise FileNotFoundError(self.destination)
        self.create_dir = create_dir

        self.auto_split = auto_split
        if self.auto_split > 1:
            # Prepare a list where each sublist goes to another remote
            self.splitted = []
            for _ in range(self.auto_split):
                self.splitted.append([])
            self.split_files_up(self.source)

    def split_files_up(self, folder: Path):
        if not folder.is_dir():
            raise NotADirectoryError("To auto split you have to give a directory path.")

        # This loop does not split perfectly, as i resets for each directory, if there
        # are subdirectories
        for i, item in enumerate(folder.iterdir()):
            if item.is_file():
                self.splitted[i % self.auto_split].append(item.name)
            if item.is_dir():
                self.split_files_up(item)

    def copy_files_to_servers(self):
        # Probably getting Remote object, that will actually handle logic
        # Need to see, if we need a self.server(s) for that, then no need for
        # separate number of servers input
        pass
