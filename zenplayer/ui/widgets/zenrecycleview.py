"""
Houses the ZenRecycleView class
"""
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from ui.kvloader import KVLoader


class ZenRecycleView(RecycleView):
    """
    Provides a shared component for Playlist and Library recycleviews.
    """
    handler = ObjectProperty()
    """ Object that should handle the "on_selected" method. """

    def __init__(self, **kwargs):
        KVLoader.load("ui/widgets/zenrecycleview.kv")
        super().__init__(**kwargs)


class SelectableLabel(RecycleDataViewBehavior, Label):
    """
    Add selection support to the Label
    """
    index = None
    """ The index of the active label in the RecycleViews' data property """

    back_color = ListProperty([0, 0, 0, 1])

    selected = BooleanProperty(False)
    """ Indicates whether this item has been selected or not. """

    handler = None
    """
    Reference to the obejct that should handle the events generated by the
    RecyleView, namely:

        * item_selected(item)
        * item_touched(item)
        * item_draw(item)
    """

    def item_draw(self):
        """ Handle the setting of the label back_color, so we call pull this
        logic out of the recycleview rabbit hole.
        """
        if self.selected:
            self.back_color = [.5, .5, 1.0, .3]
        else:
            self.back_color = [0, 0, 0, 1]

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected
        handler = self.handler = rv.handler
        if is_selected and hasattr(handler, "item_selected"):
            handler.item_selected(self)
        if hasattr(handler, "item_draw"):
            if handler.item_draw(self):
                return
        self.item_draw()

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos):
            if self.handler and hasattr(self.handler, "item_touched"):
                self.handler.item_touched(self)
            return self.parent.select_with_touch(self.index, touch)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
