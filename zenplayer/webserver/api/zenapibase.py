"""
Houses the base class for ZenPlayer classes presenting a API Interface
"""

from flask import make_response, jsonify, send_file, request
from urllib.parse import unquote
from kivy.clock import Clock
from kivy.logger import Logger


class ZenAPIBase:
    """
    The Base class for ZenPlayer object presenting an API interface. This class
    sets up the *ctrl* and "app* objects.
    """

    def __init__(self, ctrl):
        super().__init__()
        self.ctrl = ctrl
        """ Reference to the controller object. """

    @staticmethod
    def get_request_arg(key, default=""):
        """Get the request argument, being sure to unescape the URL encoded
        value."""
        return unquote(request.args.get(key, default))

    @staticmethod
    def resp_from_data(data, code=200):
        """
        Generate and return the appropriate HTTP response object containing the
        json version of the *data", which can be any object be can "jsonify".
        """
        resp = make_response(jsonify(data), code)
        resp.headers.add("Access-Control-Allow-Origin", "*")
        return resp

    @staticmethod
    def resp_from_image(file_name):
        """
        Generate and return the appropriate HTTP response object containing the
        image data from the file.
        """
        resp = make_response(send_file(file_name), 200)
        resp.headers.update(
            {
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            }
        )
        return resp

    def safe_call(self, func, *args, get_response=True):
        """
        Call the given function in a clock event. Return a success reponse if
        *get_response* is True, otherwise return None
        """
        Logger.debug("zenapibase.py: Schedule call %s, args = %s", func.__name__, args)
        Clock.schedule_once(lambda dt: func(*args))
        if get_response:
            return self.resp_from_data({"status": "success"})
