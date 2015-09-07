from remote_files import RemoteFiles
from os import remove
#: Include the Dropbox SDK
from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient
from dropbox import rest as dbrest
from dropbox.exceptions import HttpError
#: API v2
#: from dropbox import Dropbox
from kivy.uix.screenmanager import Screen


class DropboxAPI(RemoteFiles):

    access_token = None
    user_id = None
    client = None
    app_key = None
    app_secret = None
    download_folder = None

    def __init__(self, app_key, app_secret, download_folder='/tmp/dropboxfiles'):
        super(DropboxAPI, self).__init__("Dropbox")
        self.app_key = app_key
        self.app_secret = app_secret
        self.authenticated = False
        self.download_folder = download_folder

    def list(self, path, recursive=False):
        if not self.authenticated:
            self.authenticate()

        return self.client.metadata(path)

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

    def authenticate(self, ntry=0, screen=None):
        flow = DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)
        authorize_url = flow.start()
        code = None
        saved_access = False
        #: Try opening a access_token saved file
        try:
            with open(self.download_folder+'/access_token', 'r') as auth_code_file:
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
                if ntry > 0:
                    return False
                print 'Trying again...'
                return self.authenticate(ntry+1, screen)

        #: API v1
        self.client = DropboxClient(self.access_token)
        #: API v2
        #: self._client = Dropbox(self._access_token)

        #: Test the connection with dropbox client
        try:
            self.client.account_info()
        except dbrest.ErrorResponse, e:
            print 'Error: {}'.format(e)
            if ntry > 1:
                return False
            print 'Trying again...'
            #: Deletes the access_token file before trying again
            if saved_access:
                remove(self.download_folder+'/access_token')
            return self.authenticate(ntry+1, screen)

        self.authenticated = True
        #: Save the access_token to a file if it wasn't set yet.
        if not saved_access:
            with open(self.download_folder+'/access_token', 'w+') as auth_code_file:
                auth_code_file.write(self.access_token)
                auth_code_file.write('\n')
                auth_code_file.write(self.user_id)

        return True

    def refresh(self):
        pass

    def download(self, path):
        if not self.authenticated:
            self.authenticate()

        while '//' in path:
            path = path.replace('//', '/')
        try:
            f = self.client.get_file(path)
            with open(self.download_folder+path, 'wb+') as out:
                out.write(f.read())
        except HttpError as err:
            print('HTTP error', err)
            return False

    # TODO: Finish this method
    def metadata_to_file(self, filename):
        if isinstance(filename, list):
            files = []
            for f in filename:
                files.append(self.metadata_to_file(f))
            return files
        else:
            pass

RemoteFiles.register(DropboxAPI)
