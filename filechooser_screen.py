from kivy.uix.screenmanager import Screen
from local_explorer import LocalFileExplorer


class FileChooserScreen(Screen):
    def __init__(self, name):
        super(FileChooserScreen, self).__init__(name=name)
        self.explorer = LocalFileExplorer()

    def select_file(self, path):
        self.explorer.load_file(path)
