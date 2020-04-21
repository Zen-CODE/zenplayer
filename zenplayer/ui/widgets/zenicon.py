"""
This module houses the ZenIcon - an image with button behaviour
"""
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from ui.kvloader import KVLoader
from kivy.properties import ListProperty
from kivy.animation import Animation


class ZenIcon(ButtonBehavior, Image):
    """
    An image button that provides animation for touch and click events.
    """
    back_color = ListProperty([1.0, 1.0, 0.0, 0.0])

    duration = 0.2
    """ The duration of the press animation """

    def __init__(self, **kwargs):
        KVLoader.load("ui/widgets/zenicon.kv")
        super().__init__(**kwargs)
        self.animation = None

    def on_state(self, widget, state):
        """ Animate the change of colour when  the image is pressed """
        if self.animation is not None:
            self.animation.cancel(self)
        if state == "down":
            print("Starting animation")
            self.animation = Animation(back_color=[1, 1, 0, 0.5],
                                       duration=self.duration)
        else:
            self.animation = Animation(back_color=[1, 1, 0, 0.0],
                                       duration=self.duration)
        self.animation.start(self)
