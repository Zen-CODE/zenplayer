"""
This module houses helper classes for the ZenPlayer RecycleView playlist.
"""
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.clock import Clock
from kivy.uix.popup import Popup


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """


class SelectableLabel(RecycleDataViewBehavior, Label):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def on_long_touch(self, rv):
        """ Event fired when the label has been held down for a long time. """
        data = rv.ctrl.playlist.get_info(index=self.index)
        PlaylistPopup(
            title="Track: {artist} - {album} - {file}".format(**data),
            ctrl=rv.ctrl,
            index=self.index).open()

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            Clock.schedule_once(
                lambda dt: self.on_long_touch(self.parent.recycleview))
            return self.parent.select_with_touch(self.index, touch)


    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class PlaylistRV(RecycleView):
    """
    The RecycleView widget embedded in the playlist.
    """
    ctrl = ObjectProperty()
    """ A reference to the controller object"""


class PlaylistPopup(Popup):
    """
    The Popup show when the playlist item is tapped and held.
    """
    ctrl = ObjectProperty()
    """ A reference to the controller object"""

    index = NumericProperty()
    """ The index of the selected track in the Playlist.queue"""

    def button_play(self):
        print("play")

    def button_info(self):
        print("info")

    def button_remove(self):
        print("remove")
