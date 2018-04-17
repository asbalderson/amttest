from collections import defaultdict


class BPHandler(object):

    bpdict = defaultdict(dict)

    @staticmethod
    def add_blueprint(blueprint, **kwargs):
        argdict = {}

        if kwargs:
            argdict.update(**kwargs)
        BPHandler.bpdict[blueprint] = argdict


    @staticmethod
    def register_blueprints(flask_app):
        for bp in BPHandler.bpdict.keys():
            flask_app.register_blueprint(bp, **BPHandler.bpdict[bp])
