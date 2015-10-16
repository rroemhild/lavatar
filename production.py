#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if 'LAVATAR_SETTINGS' not in os.environ:
    config = 'settings.py'
    os.environ['LAVATAR_SETTINGS'] = os.path.abspath(config)

from gevent.wsgi import WSGIServer
from lavatar import app

if not app.debug:
    import logging
    handler = logging.StreamHandler()
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)
    log.addHandler(handler)

host = os.environ.get('APP_HOST', '127.0.0.1')
port = os.environ.get('APP_PORT', 5000)

http_server = WSGIServer((host, port), app)
http_server.serve_forever()
