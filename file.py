class File(object):

    def __init__(self, path, extension=None, mime_type=None, root='', size='0 bytes', nbytes=0, icon='folder', is_dir=False, file_hash=None):
        self.path = path
        self.extension = extension
        self.mime_type = mime_type
        self.root = root
        self.size = size
        self.bytes = nbytes
        self.icon = icon
        self.is_dir = is_dir
        self.file_hash = file_hash

    def __str__(self):
        return 'File "{}" with size {}. '.format(self.path, self.size)

    def __unicode__(self):
        return u""+self.__str__()
