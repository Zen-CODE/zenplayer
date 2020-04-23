"""
This module houses the ZenIcon - an image with button behaviour
"""
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from ui.kvloader import KVLoader
from kivy.properties import ListProperty, StringProperty, BooleanProperty
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

    def _get_back_color(self, state):
        """ Return the backcolor for the icon given it's state """
        if state == "down":
            return [1, 1, 0, 0.5]
        else:
            return [1, 1, 0, 0.0]

    def on_state(self, widget, state):
        """ Animate the change of colour when  the image is pressed """
        if self.animation is not None:
            self.animation.cancel(self)
        self.animation = Animation(back_color=self._get_back_color(state),
                                   duration=self.duration)
        self.animation.start(self)


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

    selected = BooleanProperty(False)
    """ Indicated when the button is selected on not """

    def on_group(self, widget, group):
        """ Allocate the obejct to a group for maintaining single selection """
        if group:
            lst = ZenSelectableIcon._groups.get(group, [])
            lst.append(widget)
            ZenSelectableIcon._groups[group] = lst
        else:
            raise NotImplementedError()

    def _set_selected(self):
        """ Set this wiget as the only one selected in it's group """
        for widget in ZenSelectableIcon._groups.get(self.group, []):
            widget.selected = bool(self == widget)

    def _get_back_color(self, state):
        """ Return the backcolor for the icon given it's state """
        if self.selected:
            return [0, 1, 0, 0.25]
        else:
            return super()._get_back_color(state)

    def on_state(self, widget, state):
        """ Animate the change of colour when  the image is pressed """
        if state == "down":
            self._set_selected()
        super().on_state(widget, self.state)
