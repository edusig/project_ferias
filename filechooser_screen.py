from os.path import expanduser

from local_explorer import LocalFileExplorer
from kivy.uix.screenmanager import Screen


class FileChooserScreen(Screen):

    def __init__(self, name):
        super(FileChooserScreen, self).__init__(name=name)
        self.explorer = LocalFileExplorer()

    #
    # Public
    #

    def preview_file(self, path):
        if len(path) is 0:
            return None
        return path[0]

    def select_file(self, path):
        self.explorer.load_file(path)

    def select_filter(self, filter_type='*'):
        if filter_type is '*':
            del self.ids.filechooser_iconview.filters[:]
            return
        self.ids.filechooser_iconview.filters = [
            '*' + x for x in self.explorer.suported_extentions(filter_type)]

    def home_path(self):
        return expanduser('~')
