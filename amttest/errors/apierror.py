from flask import jsonify


class APIError(Exception):

    def __init__(self, message, **kwargs):
        self.message = message
        if kwargs:
            self.__dict__.update(kwargs)


    def to_json(self):
        print(self.__dict__)
        return jsonify(self.__dict__)
