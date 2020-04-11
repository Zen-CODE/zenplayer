"""
This module houses shared components that across multiple UI components.
"""
from kivy.lang import Builder
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview import RecycleView
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.label import Label


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


class SelectableLabel(RecycleDataViewBehavior, Label):
    """ Add selection support to the Label """
    index = None
    back_color = ListProperty([0, 0, 0, 1])
    selected = BooleanProperty(False)

    def _set_back_color(self):
        """ Set the back color of the label considering the playlist """
        if self.selected:
            self.back_color = [.5, .5, 1.0, .3]
        else:
            self.back_color = [0, 0, 0, 1]

    def on_selected(self, _widget, _value):
        self._set_back_color()

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected


class ZenRecycleView(RecycleView):
    """
    Provides a shared component for Playlist and Library recycleviews.
    """
    ctrl = ObjectProperty()