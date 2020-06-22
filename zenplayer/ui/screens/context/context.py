"""
This module houses the Zen Music Library browser based on the recycleview
"""
from ui.screens.zenscreen import ZenScreen
from kivy.properties import StringProperty, ListProperty
from ui.widgets.zenkeydown import ZenKeyDown


class ContextScreen(ZenKeyDown, ZenScreen):
    """
    Displays a interface for viewing and interacting with the `Library`
    component
    """
    title = StringProperty("Context title")
    """ The artist for which to display the ALbum """

    actions = ListProperty()
    """ A list or dicts, with *text* and *action properties, where the *text*
    is what is displayed and the *action* the function called if that text
    is selected."""

    parent_screen = StringProperty()
    """ The name of the parent screen to show after the popup has been
    dismissed.
    """

    def __init__(self, **kwargs):
        super(ContextScreen, self).__init__(**kwargs)
        self.ids.rv.data = self.actions

    def item_touched(self, item):
        """
        The item has been selected, so perform the corresponding action and show
        the previous screen.
        """
        self.actions[item.index]["action"]()
        self.ctrl.zenplayer.show_screen(self.parent_screen)