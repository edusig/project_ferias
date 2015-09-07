from abc import ABCMeta, abstractmethod


class FileExplorer:
    """File manipulation helper class

    A class to help manipulate files within a more complex system

    Attributes:
        base_path: the prefix/working path
        current_dir: the current directory
    """

    __metaclass__ = ABCMeta

    def __init__(self, base_path='/', current_dir=''):
        """Set default values for the base path and the current directory"""
        self.base_path = base_path
        self.current_dir = current_dir

    @abstractmethod
    def list(self, path):
        """List directories and files from the current path + additional path

        Args:
            path: path from where the files and folders will be listed.

        Returns:
            list: List containing all files or directories found

        Raises:
            NotImplementedError: When this method is not implemented inside a subclass.

        Examples:
            list(True, False, "") #["usr", "var", "local", "lib"]
            list(False, True, "") #["config.json", "example.png"]

        """
        raise NotImplementedError()

    @abstractmethod
    def open(self, filename):
        """Opens a file or directory.

        Args:
            filename: str: name of the file selected to be opened

        Returns:
            The opened file or False if it could not open

        Raises:
            NotImplementedError: When this method is not implemented inside a subclass.

        Examples:
            open("image.png")
            open("/home/user/downloads/")

        """
        raise NotImplementedError()

    @abstractmethod
    def back(self):
        """Goes back to the last directory opened

        Returns:
            Success confirmation.

        Raises:
            NotImplementedError: When this method is not implemented inside a subclass.

        """
        raise NotImplementedError()

    @abstractmethod
    def detail(self, filename):
        """Returns a dictionary with more information about the file or directory.

        Args:
            filename: name of the file selected to get more information

        Returns:
            Dictionary with details of the file.

        Raises:
            NotImplementedError: When this method is not implemented inside a subclass.

        Examples:
            detail("example.png") #{size:58.000.000, permission:0777}
        """
        raise NotImplementedError()

    @abstractmethod
    def preview_file(self, filename):
        """Opens a preview of the file or an error if its a directory.

        Args:
            filename: name of the file selected to be previewed

        Returns:
            Success confirmation

        Raises:
            NotImplementedError: When this method is not implemented inside a subclass.

        Examples:
            preview_file("example.png") #shows preview of the image
        """
        raise NotImplementedError()

    @abstractmethod
    def filter(self, extension, maxsize=-1, minsize=-1):
        """Returns a list of files and directories filtered by extension or size

        Args:
            extension: file extension. Set as False to exclude from filtering by extension.
            maxsize: maximum file size. Set as -1 for no maximum file size in bytes.
            minsize: minimum file size. Set as -1 for no minimum file size in bytes.

        Returns:
            A list of filtered files

        Raises:
            NotImplementedError: When this method is not implemented inside a subclass.

        Examples:
            filter(".pdf", 157.000, -1)
        """
        raise NotImplementedError()

    @abstractmethod
    def search(self, filename, additional_path):
        """Search for a file inside a directory, default is current directory.

        Args:
            filename: name of the file you are searching.
            additional_path: suffix for the path where the file will be searched

        Returns:
            A lists of found files that match that filename

        Raises:
            NotImplementedError: When this method is not implemented inside a subclass.

        Examples:
            search("example", "downloads") #["example.png"]
        """
        raise NotImplementedError()
