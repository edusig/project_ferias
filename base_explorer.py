import os

from file import File
from abc import ABCMeta, abstractmethod


class BaseFileExplorer:
    """File manipulation helper class

    A class to help manipulate files within a more complex system

    Attributes:
        base_path: the prefix/working path
        current_dir: the current directory
    """

    __metaclass__ = ABCMeta

    #: TODO: Verify actual supported file types on a raspberry pi.
    supported_file_types = {
        'presentation': {
            'extensions': ['.ppt',
                           '.pptx',
                           '.pdf',
                           '.odp'],
            'mime_types': ['application/mspowerpoint',
                           ('application/vnd.openxmlformats-officedocument'
                            '.presentationml.presentation'),
                           'application/pdf'
                           'application/vnd.oasis.opendocument.presentation']
        },
        'music': {
            'extensions': ['.3gp',
                           '.3ga',
                           '.aiff',
                           '.aif',
                           '.aifc',
                           '.aac',
                           '.au',
                           '.amr',
                           '.flac',
                           '.mp3',
                           '.ogg',
                           '.oga',
                           '.opus',
                           '.ra',
                           '.ram',
                           '.snd',
                           '.tta',
                           '.wav',
                           '.wave',
                           '.webm',
                           '.wma'],
            'mime_types': ['audio/3gpp',
                           'audio/3gpp2',
                           'audio/aiff',
                           'audio/x-aiff',
                           'audio/aac',
                           'audio/aacp',
                           'audio/basic',
                           'audio/amr',
                           'audio/x-flac',
                           'audio/mpeg3',
                           'audio/ogg',
                           'audio/opus',
                           'audio/vnd.rn-realaudio',
                           'audio/x-pn-realaudio',
                           'audio/x-tta',
                           'audio/vnd.wave',
                           'audio/wav',
                           'audio/wave',
                           'audio/x-wav',
                           'audio/webm',
                           'audio/x-ms-wma']
        },
        'video': {
            'extensions': ['.mp4',
                           '.avi',
                           '.webm',
                           '.mkv',
                           '.flv',
                           '.gif',
                           '.mov',
                           '.qt',
                           '.rmvb',
                           '.mpeg',
                           '.mpg',
                           '.mp2',
                           '.mpe',
                           '.mpv',
                           '.m2v',
                           '.wmv',
                           '.ogg',
                           '.ogv'],
            'mime_types': ['video/mp4',
                           'application/x-troff-msvideo',
                           'video/avi',
                           'video/msvideo',
                           'video/x-msvideo',
                           'video/webm',
                           'video/x-matroska',
                           'video/x-flv',
                           'image/gif',
                           'video/quicktime',
                           'application/vnd.rn-realmedia-vbr',
                           'video/mpeg',
                           'video/x-ms-wmv',
                           'video/vnd.avi',
                           'video/ogg',
                           'application/ogg',
                           ]
        },
        'image': {
            'extensions': ['.jpg',
                           '.jpeg',
                           '.bm'
                           '.bmp',
                           '.png',
                           '.gif',
                           '.webp',
                           '.svg'],
            'mime_types': ['image/jpeg',
                           'image/pjpeg',
                           'image/bmp',
                           'image/x-windows-bmp'
                           'image/png',
                           'image/gif',
                           'image/webp',
                           'image/svg+xml']
        }
    }

    def __init__(self, base_path='/', current_dir=[]):
        """Set default values for the base path and the current directory"""
        self.base_path = base_path
        self.current_dir = current_dir
        self.supported_file_types['presentation']['open'] = self._open_presentation
        self.supported_file_types['music']['open'] = self._open_music
        self.supported_file_types['image']['open'] = self._open_image
        self.supported_file_types['video']['open'] = self._open_video

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
        if isinstance(filename, File):
            path = filename.path
            is_dir = filename.is_dir
        else:
            path = filename
            is_dir = os.path.isdir(path)

        #: If it is a directory, return a list of files.
        if is_dir:
            if isinstance(self.current_dir, list):
                self.current_dir.append(path)
            else:
                self.current_dir = [self.current_dir, path]
            return self.list(self.current_dir[-1])

        name, extension = os.path.splitext(path)
        for file_type in self.supported_file_types:
            if extension in self.supported_file_types[file_type]['extensions']:
                self.supported_file_types[file_type]['open'](filename)

    def back(self):
        """Goes back to the last directory opened

        Returns:
            Success confirmation.

        Raises:
            NotImplementedError: When this method is not implemented inside a subclass.

        """
        self.current_dir.pop()
        self.open(self.current_dir[-1])

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
            extension:  file extension.
                        Set as False to exclude from filtering by extension.
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

    @staticmethod
    def check_or_create_folder(path):
        #: Check if folder exists
        if not os.access(path, os.F_OK):
            os.makedirs(path)
        else:
            #: If it exists, check if it is actually a folder
            if not os.path.isdir(path):
                raise OSError('{} is not a folder!'.format(path))

        #: Check if folder is writeable
        if not os.access(path, os.W_OK):
            os.chmod(path, 0777)
            os.chown(path, os.getuid(), os.getgid())
            #: Check if still isn't writeable, meaning the actions above had no effect
            if not os.access(path, os.W_OK):
                raise OSError('Could not write the base folder and could not '
                              'change its owner or access rights')

    def _open_presentation(self, filename):
        print "open presentation. {}".format(filename)

    def _open_music(self, filename):
        print "open music. {}".format(filename)

    def _open_image(self, filename):
        print "open image. {}".format(filename)

    def _open_video(self, filename):
        print "open video. {}".format(filename)
