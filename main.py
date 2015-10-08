__version__ = '0.0.1'

from kivy import properties
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix import settings
from kivy.lang import Builder

# XXX: This import is related to fullscreen
# from kivy.config import Config

import main_screen
import filechooser_screen


class Main(BoxLayout):

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.ids.screen_manager.add_widget(main_screen.MainScreen(name='main_screen'))
        self.ids.screen_manager.add_widget(filechooser_screen.FileChooserScreen
                                           (name='filechooser_screen'))


class PresenterApp(App):

    use_kivy_settings = False

    #
    #   Properties
    #

    title = properties.StringProperty('Opuntia')

    #
    #   App implementation
    #

    def build(self):
        # This line activated the full screen mode
        # Config.set('graphics', 'fullscreen', 'auto')
        self.icon = 'data/pixmaps/icon.png'
        Builder.load_file('data/opuntia_ui.kv')
        root = Main()
        return root


if __name__ == '__main__':
    app = PresenterApp()
    try:
        app.run()
    except KeyboardInterrupt:
        app.stop()
