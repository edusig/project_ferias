from file_explorer import FileExplorer
from abc import abstractmethod


class RemoteFiles(FileExplorer):

    application_name = None
    cache_files = []
    refresh_time = 3600
    authenticated = False

    def __init__(self, application_name):
        super(RemoteFiles, self).__init__()
        self.application_name = application_name

    @abstractmethod
    def authenticate(self):
        raise NotImplementedError()

    @abstractmethod
    def refresh(self):
        raise NotImplementedError()

    @abstractmethod
    def download(self, path):
        raise NotImplementedError()


FileExplorer.register(RemoteFiles)
