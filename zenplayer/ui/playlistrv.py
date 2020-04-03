"""
This module houses helper classes for the ZenPlayer RecycleView playlist.
"""
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.clock import Clock


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """


class SelectableLabel(RecycleDataViewBehavior, Label):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(SelectableLabel, self).__init__(**kwargs)
        self.register_event_type('on_long_touch')

    def on_long_touch(self, *args):
        """ Event fired when the label has been held down for a long time. """
        print("on_long_touch fired!")

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
            # Set a timer to generate the long_touch event
            touch.long_touch = Clock.schedule_once(
                lambda dt: self.dispatch("on_long_touch"), 1)
            return self.parent.select_with_touch(self.index, touch)

    def on_touch_up(self, touch):
        """ Prevent firing of the `on_long_touch` event. """
        event = getattr(touch, "long_touch", None)
        if event is not None:
            event.cancel()
        return super(SelectableLabel, self).on_touch_up(touch)

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
