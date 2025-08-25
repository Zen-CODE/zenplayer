"""
This module houses the ZenIcon - an image with button behaviour
"""

from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from ui.kvloader import KVLoader
from kivy.properties import ListProperty, StringProperty, BooleanProperty
from kivy.animation import Animation


ICON_BACKCOLOR = [1.0, 0.0, 0.0, 0.0]
ICON_COLOR = [0.5, 0.5, 1.0, 1.0]


class ZenIcon(ButtonBehavior, Image):
    """
    An image button that provides animation for touch and click events.
    """

    back_color = ListProperty(ICON_BACKCOLOR)
    color = ListProperty(ICON_COLOR)

    duration = 0.2
    """ The duration of the press animation """

    selected = BooleanProperty(False)
    """ Indicated when the button is selected on not """

    def __init__(self, **kwargs):
        KVLoader.load("ui/widgets/zenicon.kv")
        super().__init__(**kwargs)
        self.animation = None
        self.mipmap = True

    def _get_back_color(self):
        """Return the backcolor for the icon given it's state"""
        if self.state == "down" or self.selected:
            return [0, 1, 0, 0.7]
        else:
            return [0, 1, 0, 0.0]

    def draw_widget(self):
        """Set the back_color of the widget preventing clashing animations"""
        if self.animation is not None:
            self.animation.cancel(self)
        self.animation = Animation(
            back_color=self._get_back_color(), duration=self.duration
        )
        self.animation.start(self)

    def on_state(self, widget, state):
        """Animate the change of colour when  the image is pressed"""
        self.draw_widget()

    def on_selected(self, widget, value):
        """Animate the change of colour when  the icon is selected"""
        self.draw_widget()


class ZenSelectableIcon(ZenIcon):
    """
    An image button that provides animation for touch and click events.
    """

    group = StringProperty(None)
    """
    Set the name for a group of selectable icons, where only one of them
    can be selected at any time.

    Note: This should not be changed once set. Dynamic allocation is not yet
          supported.
    """

    _groups = {}
    """ A dictionary of group names used to maintain selection data """

    def on_group(self, widget, group):
        """Allocate the obejct to a group for maintaining single selection"""
        if group:
            lst = ZenSelectableIcon._groups.get(group, [])
            lst.append(widget)
            ZenSelectableIcon._groups[group] = lst
        else:
            raise NotImplementedError()

    def _set_selected(self):
        """Set this wiget as the only one selected in it's group"""
        for widget in ZenSelectableIcon._groups.get(self.group, []):
            widget.selected = bool(self == widget)

    def _get_back_color(self):
        """Return the backcolor for the icon given it's state"""
        if self.selected:
            return [1, 1, 0, 0.35]
        else:
            return super()._get_back_color()

    def on_state(self, widget, state):
        """Animate the change of colour when  the image is pressed"""
        if state == "down":
            self._set_selected()
        else:
            super().on_state(widget, state)

    def on_selected(self, _widget, _value):
        """Trigger the redrawing of the widget on selection changes"""
        self.draw_widget()
