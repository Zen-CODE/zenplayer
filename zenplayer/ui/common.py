"""
This module houses shared components that across multiple UI components.
"""
from kivy.lang import Builder
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior


class Common:
    """
    Handles the loading of commond components.
    """
    _loaded = False

    def load_common():
        """ Load commond kv, ensuring not to do it multiple times. """
        if not Common._loaded:
            Builder.load_file("ui/common.kv")
            Common._loaded = True


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
