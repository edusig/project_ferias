#: Include the Dropbox SDK
from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient
from dropbox import rest as dbrest
from dropbox.exceptions import HttpError
from file import File
from kivy.uix.screenmanager import Screen
from os import remove
from os.path import splitext
from remote_file import RemoteFile
from remote_files import RemoteFiles
from urllib2 import HTTPError


class DropboxAPI(RemoteFiles):

    def __init__(self, app_key, app_secret, base_folder='/opuntia/dropboxfiles'):
        super(DropboxAPI, self).__init__("Dropbox", base_folder)
        self.app_key = app_key
        self.app_secret = app_secret
        self.authenticated = False
        self.client = None
        self.user_id = None
        self.access_token = None

    def list(self, path, recursive=False):
        if not self.authenticated:
            self.authenticate()

        return self.metadata_to_file(self.client.metadata(path))

    def open(self, filename):
        pass

    def back(self):
        pass

    def detail(self, filename):
        pass

    def preview_file(self, filename):
        pass

    def filter(self, extension, maxsize=-1, minsize=-1):
        pass

    def search(self, filename, additional_path):
        pass

    def authenticate(self, authentication_attempts=2, connection_attempts=2, screen=None):
        flow = DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)
        authorize_url = flow.start()
        code = None
        saved_access = False
        #: Try opening a access_token saved file
        try:
            with open(self.base_folder+'/access_token', 'r') as auth_code_file:
                self.access_token = auth_code_file.readline().replace('\n', '')
                self.user_id = auth_code_file.readline()
                saved_access = True
        #: If it doesn't exist, start a new authentication flow
        except(IOError, OSError):
            self.access_token = None
            if screen is not None and isinstance(screen, Screen):
                # TODO: Open a kivy popup with a browser to authenticate dropbox
                print "Screen received!"
            else:
                print '1. Go to the url: {}'.format(authorize_url)
                print '2. Click "Allow" (you might have to log in first).'
                print '3. Copy the authorization code.'
                code = raw_input("Enter authorization code here: ").strip()

            #: Test the authentication code
            try:
                self.access_token, self.user_id = flow.finish(code)
            except dbrest.ErrorResponse, e:
                print 'Error: {}'.format(e)
                if authentication_attempts <= 0:
                    return False
                print 'Trying again...'
                return self.authenticate(authentication_attempts-1, connection_attempts, screen)

        #: API v1
        self.client = DropboxClient(self.access_token)
        #: API v2
        #: self._client = Dropbox(self._access_token)

        #: Test the connection with dropbox client
        try:
            self.client.account_info()
        except dbrest.ErrorResponse, e:
            print 'Error: {}'.format(e)
            if authentication_attempts <= 0:
                return False
            print 'Trying again...'
            #: Deletes the access_token file before trying again
            if saved_access:
                remove(self.base_folder+'/access_token')
            return self.authenticate(authentication_attempts, connection_attempts-1, screen)

        self.authenticated = True
        #: Save the access_token to a file if it wasn't set yet.
        if not saved_access:
            with open(self.base_folder+'/access_token', 'w+') as auth_code_file:
                auth_code_file.write(self.access_token)
                auth_code_file.write('\n')
                auth_code_file.write(self.user_id)

        return True

    def refresh(self):
        pass

    def download(self, path):
        if not self.authenticated:
            self.authenticate()

        rfile = None
        if isinstance(path, RemoteFile):
            rfile = path
            path = rfile.path
        elif isinstance(path, File):
            raise TypeError("For remote services use RemoteFile object")

        while '//' in path:
            path = path.replace('//', '/')
        try:
            f = self.client.get_file(path)
            with open(self.download_folder+path, 'wb+') as out:
                out.write(f.read())
        except HttpError as err:
            raise HTTPError(err)

        if rfile is None:
            rfile = RemoteFile(self.download_folder+path, path)

        self.cached_files.append(rfile)

    def metadata_to_file(self, metadata):
        files = []
        #: If it is a list of files call this method again for each file
        if isinstance(metadata, list):
            for f in metadata:
                #: Since this method always returns a list,
                #: it only has to append the first element.
                files.append(self.metadata_to_file(f)[0])
            return files
        else:
            filename, file_extension = splitext(metadata['path'])
            rf = RemoteFile(metadata['path'], metadata['path'])
            rf.root = self.download_folder
            rf.extension = file_extension

            if 'size' in metadata:
                rf.size = metadata['size']

            if 'modified' in metadata:
                rf.last_modified = metadata['modified']

            if 'bytes' in metadata:
                rf.bytes = metadata['bytes']

            if 'mime_type' in metadata:
                rf.mime_type = metadata['mime_type']

            if 'is_dir' in metadata:
                rf.is_dir = metadata['is_dir']

            if 'hash' in metadata:
                rf.file_hash = metadata['hash']

            if 'rev' in metadata:
                rf.modification_identifier = metadata['rev']

            files.append(rf)
            if 'contents' in metadata:
                for mfile in self.metadata_to_file(metadata['contents']):
                    files.append(mfile)
        return files

RemoteFiles.register(DropboxAPI)
