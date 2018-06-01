#!/usr/bin/env python3

from amttest import amttest


amttest.setup_logging(debug=False, verbose=True)
app = amttest.config_app('amttest')
amttest.BPHandler.register_blueprints(app)
amttest.config_dabase(app)
application = app

# sudo apt install libapache2-mod-wsgi-py3
"""
"<VirtualHost *>
    #ServerName example.com

    WSGIDaemonProcess amttest user=amttest group=amttest threads=5
    WSGIScriptAlias / /var/www/amttest/amttest.wsgi

    <Directory /var/www/amttest>
        WSGIProcessGroup amttest
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>
"""
