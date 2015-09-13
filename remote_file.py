from file import File
from datetime import datetime


class RemoteFile(File):

    def __init__(self, path, remote_path, extension=None, mime_type=None, root='', size='0 bytes',
                 nbytes=0, icon='folder', preview_cache=None, modification_identifier=None):
        super(RemoteFile, self).__init__(path, extension, mime_type, root, size, nbytes, icon)
        self.cached_at = datetime.now()
        self.remote_path = remote_path
        self.preview_cache = preview_cache
        self.modification_identifier = modification_identifier

    def __str__(self):
        return 'Remote File "{}" with size {}. '.format(self.path, self.size)

    def __unicode__(self):
        return u""+self.__str__()
