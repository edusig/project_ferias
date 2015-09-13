from file_explorer import FileExplorer
from abc import abstractmethod
import tempfile
from file import File
from remote_file import RemoteFile
import os
from urllib2 import HTTPError


class RemoteFiles(FileExplorer):

    def __init__(self, application_name, base_folder='/opuntia'):
        super(RemoteFiles, self).__init__()
        self.application_name = application_name
        self.base_folder = tempfile.gettempdir()+base_folder
        self.download_folder = self.base_folder+'/files'
        self.cached_files = []
        self.refresh_time = 3600
        self.authenticated = False
        self.check_or_create_folder(self.base_folder)
        self.check_or_create_folder(self.download_folder)

    def open(self, filename):

        is_dir, path = self._get_path_filename(filename)

        #: If it is a directory, return a list of files.
        if is_dir:
            if isinstance(self.current_dir, list):
                self.current_dir.append(path)
            else:
                self.current_dir = [self.current_dir, path]
            return self.list(self.current_dir)

        #: If file doesn't exists, try downloading it.
        if not os.access(self.download_folder+path, os.F_OK):
            try:
                self.download(path)
            except HTTPError as error:
                raise IOError("Could not download remote file. Try again!", error)

        super(RemoteFiles, self).open(self.download_folder+path)
        return True

    #: TODO: Finish this method. Consider implementing only on the subclasses.
    def detail(self, filename):

        is_dir, path = self._get_path_filename(filename)

        f = self._search_cached_files(path)
        if not f:
            if not is_dir:
                self.download(path)

    @abstractmethod
    def authenticate(self):
        raise NotImplementedError()

    @abstractmethod
    def refresh(self):
        raise NotImplementedError()

    @abstractmethod
    def download(self, path):
        raise NotImplementedError()

    @staticmethod
    def _get_path_filename(filename):
        if isinstance(filename, RemoteFile):
            path = filename.remote_path
            is_dir = filename.is_dir
        elif isinstance(filename, File):
            raise TypeError("For remote services use RemoteFile object")
        else:
            path = filename
            is_dir = os.path.isdir(path)
        return tuple(is_dir, path)

    def _search_cached_files(self, path):
        for f in self.cached_files:
            if f.path == path:
                return f
        return False


FileExplorer.register(RemoteFiles)
