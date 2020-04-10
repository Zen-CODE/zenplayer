"""
Houses the base class for ZenPlayer classes presenting a API Interface
"""


class ZenAPIBase:
    """
    The Base class for ZenPlayer object presenting an API interface. This class
    sets up the *ctrl* and "app* objects.
    """
    def __init__(self, ctrl, app):
        super(ZenAPIBase, self).__init__()
        self.ctrl = ctrl
        """ Reference to the controller object. """
        self.app = app
        """ Reference to the flask app context. """
