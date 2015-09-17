import os
import subprocess

from kivy import properties
from kivy.uix.screenmanager import Screen


class Type_Selector(Screen):
    app = properties.ObjectProperty()

    extensions = {
        'presentation': ['.ppt',
                         '.pptx',
                         '.pdf',
                         '.odp'],

        'music': ['.mp3'],

        'video': ['.mp4',
                  '.avi'],

        'image': ['.jpg',
                  '.jpeg',
                  '.bmp',
                  '.png'],
    }

    #
    #   Public
    #

    def filter_selected(self, filter_type=['*']):
        del self.ids.file_chooser.filters[:]
        for i in filter_type:
            self.ids.file_chooser.filters.append(i)

    def go_back(self):
        self.manager.current = 'source_screen'

    def load_file(self, filename):
        path = str(filename.pop())
        name, extension = os.path.splitext(path)
        if extension in self.extensions['presentation']:
            self._load_presenter(path, extension)
            return

        if extension in self.extensions['music']:
            self._load_music(path)
            return

        if extension in self.extensions['video']:
            self._load_video(path)
            return

        if extension in self.extensions['image']:
            self._load_image(path)
            return

    def preview_file(self, filename):
        if len(filename) is 0:
            return None
        return filename[0]

    #
    #   Private
    #

    # XXX: Quando os testes forem feitos no RPi eh necessarios listar e alterar os
    # leitores de formatos para sua utilizacao.
    def _load_image(self, filename):
        subprocess.call(['eog', '-f', filename], shell=False)

    def _load_music(self, filename):
        subprocess.call(['totem', filename], shell=False)

    def _load_presenter(self, filename, extension):
        print type(extension)
        if extension == '.pdf':
            subprocess.call(['xpdf', '-fullscreen', filename], shell=False)
            return

        subprocess.call(['libreoffice', '--nologo', '--show', filename], shell=False)

    def _load_video(self, filename):
        subprocess.call(['totem', filename], shell=False)
