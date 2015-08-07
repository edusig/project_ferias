import os
import subprocess

from kivy import properties
from kivy.uix.screenmanager import Screen


class Type_Selector(Screen):
    app = properties.ObjectProperty()

    presentation_formats = ['.ppt',
                            '.pptx',
                            '.pdf',
                            '.odp']
    music_formats = ['.mp3']

    video_formats = ['.mp4',
                     '.avi']

    image_formats = ['.jpg',
                     '.jpeg',
                     '.bmp',
                     '.png']

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
        if extension in self.presentation_formats:
            self._load_presenter(path, extension)
            return

        if extension in self.music_formats:
            self._load_music(path)
            return

        if extension in self.video_formats:
            self._load_video(path)
            return

        if extension in self.image_formats:
            self._load_image(path)
            return

    def preview_file(self, filename):
        if len(filename) is 0:
            return None
        return filename[0]

    #
    #   Private
    #

    # XXX Quando os testes forem feitos no RPi é necessários listar e alterar os
    # leitores de formatos para sua utilização.
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
