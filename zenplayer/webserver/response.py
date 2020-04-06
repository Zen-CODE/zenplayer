"""
This module provide helper classes for building flask reponses.
"""
from flask import make_response, jsonify, send_file


class Response:
    """
    A convenience class for building generic flask reponses
    """
    @staticmethod
    def from_dict(app, data_dict, code=200):
        """
        Generate and return the appropriate HTTP response object containing the
        json version of the *data_dict" dictionary.
        """
        with app.app_context():
            resp = make_response(jsonify(data_dict), code)
            resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp

    @staticmethod
    def from_image(app, file_name):
        """
        Generate and return the appropriate HTTP response object containing the
        image data from the file.
        """
        with app.app_context():
            resp = make_response(send_file(file_name), 200)
            resp.headers.update({
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'})
        return resp
