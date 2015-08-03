__version__ = '0.0.1'
import kivy

from kivy import properties
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
#from kivy.uix import settings
#from kivy.uix.widget import Widget
from kivy.lang import Builder

import source_screen, type_selector, status_bar


class Main(BoxLayout):

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.ids.screen_manager.add_widget(source_screen.Source_Screen(name='source_screen'))


class PresenterApp(App):

    use_kivy_settings = False

    #
    #   Properties
    #

    title = properties.StringProperty('Presenter')

    #
    #   App implementation
    #

    def build(self):
        Builder.load_file('visual.kv')
        root = Main()
        return root

    #
    #   Callbacks
    #


if __name__ == '__main__':
    app = PresenterApp()
    try:
        app.run()
    except KeyboardInterrupt:
        app.stop()
