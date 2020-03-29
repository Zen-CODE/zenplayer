"""
This module provide helper classes for building flask reponses.
"""
from flask import make_response, jsonify


class Response:
    """
    A convenience class for building generic flask reponses
    """
    def from_dict(self, data_dict, code=200):
        """
        Generate and return the appropriate HTTP response object containing the
        json version of the *data_dict" dictionary.
        """
        data_dict.update(self.get_state())
        with self.app.app_context():
            resp = make_response(jsonify(data_dict), code)
            resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp
