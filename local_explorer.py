import subprocess

from kivy import properties
from base_explorer import BaseFileExplorer


class LocalFileExplorer(BaseFileExplorer):

    app = properties.ObjectProperty()

    def __init__(self):
        super(LocalFileExplorer, self).__init__()

    #
    #   Public
    #

    def filter_selected(self, filter_type=['*']):
        del self.ids.file_chooser.filters[:]
        for i in filter_type:
            self.ids.file_chooser.filters.append('*' + i)

    def go_back(self):
        self.manager.current = 'source_screen'

    def load_file(self, filename):
        self.open(str(filename.pop()))

    def preview_file(self, filename):
        if len(filename) is 0:
            return None

    def list(self, path):
        pass

    def detail(self, filename):
        pass

    def filter(self, extension, maxsize=-1, minsize=-1):
        pass

    def search(self, filename, additional_path):
        pass

    #
    #   Private
    #

    # XXX: Quando os testes forem feitos no RPi eh necessarios listar e alterar os
    # leitores de formatos para sua utilizacao.
    def _open_presentation(self, filename):
        if filename == '.pdf':
            subprocess.call(['xpdf', '-fullscreen', filename], shell=False)
            return

        subprocess.call(['libreoffice', '--nologo', '--show', filename], shell=False)
        print "open presentation. {}".format(filename)

    def _open_music(self, filename):
        subprocess.call(['totem', filename], shell=False)
        print "open music. {}".format(filename)

    def _open_image(self, filename):
        subprocess.call(['eog', '-f', filename], shell=False)
        print "open image. {}".format(filename)

    def _open_video(self, filename):
        subprocess.call(['totem', filename], shell=False)
        print "open video. {}".format(filename)

BaseFileExplorer.register(LocalFileExplorer)
