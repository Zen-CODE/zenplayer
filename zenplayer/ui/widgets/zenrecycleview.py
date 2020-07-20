"""
Houses the ZenRecycleView class
"""
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from ui.kvloader import KVLoader
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import BooleanProperty


class ZenRecycleView(FloatLayout):
    """
    Provides a shared component for Playlist and Library recycleviews.
    """
    handler = ObjectProperty()
    """ Object that should handle the "on_selected" method. """

    data = ObjectProperty([])
    """ The data synchronized with the recycleview """

    search_text = StringProperty("")
    """
    Text entered by the user to move to the first artist staring with the
    text.
    """
    note_text = StringProperty("Loading library. Please wait..")
    """
    The text, obtained from the keyboard, for searched for items in the list
    of atists.
    """

    show_note = BooleanProperty(True)
    """
    Boolean property dictating whether or not the notification label should
    be dispalyed.
    """

    def __init__(self, **kwargs):
        KVLoader.load("ui/widgets/zenrecycleview.kv")
        super().__init__(**kwargs)

    def on_data(self, _widget, _value):
        """ Remove the loading warning once data is loaded. """
        self.note_text = ""

    def find_item(self, text):
        """ Jump to the first item that has a text match with *text* """
        self.ids.rv.layout_manager.clear_selection()
        length = len(self.data)
        text_lower = text.lower()
        for i, data in enumerate(self.data):
            if data["text"].lower().find(text_lower) > -1:
                if length > 10:  # Only scroll if required
                    self.ids.rv.scroll_y = 1.0 - 1.005 * float(i) / float(
                        length)
                Clock.schedule_once(lambda dt: self._select_item(text_lower))
                return

    def _select_item(self, text_lower):
        """ Select the first itme that contains matching text. """
        for _k, label in self.ids.rv.view_adapter.views.items():
            if label.text.lower().find(text_lower) > -1:
                label.selected = True
                return

    def on_show_note(self, widget, value):
        """ Either hide of show the note label """
        end_value = 1 if value else 0
        Animation(opacity=end_value, duration=2).start(self.ids.note_label)

    def on_note_text(self, widget, text):
        """ Handle the change of note text """
        self.show_note = bool(text)

    def on_search_text(self, widget, text):
        """ Handle the display and mechanics of searching for matches """
        if text:
            self.note_text = f"Searching for: {text}"
            self.find_item(text)
        else:
            self.note_text = ""

    def on_key_down(self, keycode, text, modifiers):
        """ Respond the pressing of a key """
        # print(f"Got keydown text: {text}, keybode={keycode}")
        if text is not None:
            self.search_text += text
        elif keycode[0] == 8 and self.search_text:  # delete
            self.search_text = self.search_text[:-1]
        elif keycode[0] == 27:  # escape
            self.search_text = ""
        elif keycode[1] == "up":
            self.ids.box_layout.move_selection(False)
        elif keycode[1] == "down":
            self.ids.box_layout.move_selection()
        elif keycode[1] == "enter":
            box = self.ids.box_layout
            if box.selected_widget:
                box.handle_event("item_touched", box.selected_widget)
        elif keycode[1] == "backspace":
            if self.handler.name == "Albums":
                self.handler.ctrl.zenplayer.show_screen("Artists")


class SelectableLabel(RecycleDataViewBehavior, Label):
    """
    Add selection support to the Label
    """
    index = None
    """ The index of the active label in the RecycleViews' data property """

    back_color = ListProperty([0, 0, 0, 1])

    selected = BooleanProperty(False)
    """ Indicates whether this item has been selected or not. """

    def _item_draw(self):
        """ Handle the setting of the label back_color, so we call pull this
        logic out of the recycleview rabbit hole.
        """
        self.back_color = [.5, .5, 1.0, .3] if self.selected else [0, 0, 0, 1]

    def on_selected(self, _widget, _value):
        """ Respond to the change of selection """
        box = self.parent
        if box and box.selected_widget:
            if box.selected_widget != self:
                self.parent.selected_widget.selected = False
        self._item_draw()
        if _value and box:
            box.selected_widget = self

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected
        if self.parent:
            self.parent.handle_event("item_selected", self, is_selected)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos):
            Clock.schedule_once(lambda dt: self.parent.handle_event(
                "item_touched", self))
            return self.parent.select_with_touch(self.index, touch)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_widget = None

    def handle_event(self, event, *args):
        """ Delegate the *event* to the handler if required.

        Args:
            event (str): One of "item_touched" or "item_selected".
        Return:
            None
        """
        handler = getattr(self.parent.parent, "handler", None)
        if handler is not None:
            meth = getattr(handler, event, None)
            if meth is not None:
                meth(*args)

    def move_selection(self, down=True):
        """ Move to the next itme in the selection."""
        rv = self.parent
        if self.selected_widget:
            if down and self.selected_widget.index < len(rv.data) - 1:
                text = rv.data[self.selected_widget.index + 1]["text"]
            elif not down and self.selected_widget.index > 0:
                text = rv.data[self.selected_widget.index - 1]["text"]
            else:
                return
        else:
            # If nothing is selected, just select the first/last
            text = rv.data[0 if down else len(rv.data) -1]["text"]
        rv.parent.find_item(text)
