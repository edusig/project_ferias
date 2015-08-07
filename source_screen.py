import os
from kivy.uix.screenmanager import Screen

class Source_Screen(Screen):

    def source_selected(self):
        self.manager.current = 'file_chooser'

    # In debian the path of external devices is /media/hostname/
    #device_name = os.listdir('')
