from werkzeug.exceptions import HTTPException
from flask import jsonify

class FyleError(HTTPException):
    code = 400
    description = 'This is a fyle error message.'

    def __init__(self, description=None, response=None):
        if description:
            self.description = description
        super().__init__(description, response)

    def get_body(self, environ=None):
        return jsonify({
            'error': 'FyleError',
            'message': self.description
        })

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

class ValidationError(HTTPException):
    code = 400
    description = 'This is a fyle error message.'

    def __init__(self, description=None, response=None):
        if description:
            self.description = description
        super().__init__(description, response)

    def get_body(self, environ=None):
        return jsonify({
            'error': 'ValidationError',
            'message': self.description
        })

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]