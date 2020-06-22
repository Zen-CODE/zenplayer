"""
This module houses the Zen Music Library browser based on the recycleview
"""
from ui.screens.zenscreen import ZenScreen
from kivy.properties import StringProperty, ListProperty
from ui.widgets.zenkeydown import ZenKeyDown
from kivy.clock import Clock


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

    def on_actions(self, widget, value):
        def set_value(dt):
            self.ids.rv.data = value
        Clock.schedule_once(set_value)

    def item_touched(self, item):
        """
        The item has been selected, so perform the corresponding action and show
        the previous screen.
        """
        item = self.actions[item.index]
        item["action"]()
        if item.get("show_parent", True):
            self.ctrl.zenplayer.show_screen(self.parent_screen)
