"""
This class houses the Playlist class for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from ui.common import SelectableLabel
from kivy.clock import Clock


class PlaylistScreen(Screen):
    """
    Displays the playlist along with some simple editing options.
    """
    ctrl = ObjectProperty()
    """ Reference to the controller """

    current = NumericProperty(-1)
    """ The index of the currently playing track in the queue. """

    def __init__(self, **kwargs):
        Builder.load_file("ui/screens/playlist/playlist.kv")
        super().__init__(**kwargs)


class PlaylistLabel(SelectableLabel):
    """ Add selection support to the Label """
    current_track = BooleanProperty(False)

    def _set_back_color(self):
        """ Set the back color of the label considering the playlist """
        if self.current_track:
            self.back_color = [.5, 1.0, .50, .3]
        else:
            super()._set_back_color()

    def on_current_track(self, _widget, _value):
        self._set_back_color()

    def on_long_touch(self, rv):
        """ Event fired when the label has been held down for a long time. """
        data = rv.ctrl.playlist.get_info(index=self.index)
        PlaylistPopup(
            title="Track: {artist} - {album} - {track}".format(**data),
            ctrl=rv.ctrl,
            index=self.index).open()

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.current_track = bool(rv.current == index)
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos):
            Clock.schedule_once(
                lambda dt: self.on_long_touch(self.parent.recycleview))
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected


class PlaylistPopup(Popup):
    """
    The Popup show when the playlist item is tapped and held.
    """
    ctrl = ObjectProperty()
    """ A reference to the controller object"""

    index = NumericProperty()
    """ The index of the selected track in the Playlist.queue"""

    def button_play(self):
        """ Play the track selected track. """
        self.ctrl.play_index(self.index)

    def button_info(self):
        """ Display detailed info on the selected track """
        data = self.ctrl.playlist.queue[self.index]
        self.ctrl.show_screen("info", filename=data["filename"])

    def button_remove(self):
        """ Play the track selected track. """
        self.ctrl.remove_index(self.index)
