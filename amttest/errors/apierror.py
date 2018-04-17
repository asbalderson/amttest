from flask import jsonify


class APIError(Exception):

    def __init__(self, message, **kwargs):
        super().__init__(self)
        self.message = message
        if kwargs:
            self.__dict__.update(kwargs)


    def to_json(self):
        return jsonify(self.__dict__)
