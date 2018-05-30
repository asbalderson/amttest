#!/usr/bin/env python3

from amttest import amttest


amttest.setup_logging(debug=False, verbose=True)
app = amttest.config_app('amttest')
amttest.BPHandler.register_blueprints(app)
amttest.config_dabase(app)
application = app
