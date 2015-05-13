__version__ = '0.0.1'
import kivy

from kivy import properties
from kivy.app import App
from kivy.uix import settings
from kivy.uix.widget import Widget
from kivy.lang import Builder


class Home(Widget):
    pass


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
        Builder.load_file('pong.kv')
        root = Home()

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

