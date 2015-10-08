import usb.core
import usb.util

from kivy.uix.screenmanager import Screen


class MainScreen(Screen):

    def source_selected(self):
        self.manager.current = 'filechooser_screen'

    # In debian the path of external devices is /media/hostname/
    # device_name = os.listdir('')
    dev = usb.core.find()
