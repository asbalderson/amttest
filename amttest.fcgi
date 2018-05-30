#!/usr/bin/env python3

from flup.server.fcgi import WSGIServer
from amttest import amttest


if __name__ == '__main__':
    amttest.setup_logging(debug=False, verbose=True)
    app = amttest.config_app('amttest')
    amttest.BPHandler.register_blueprints(app)
    amttest.config_dabase(app)
    WSGIServer(app).run()
