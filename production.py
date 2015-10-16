#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()

import os

if 'LAVATAR_SETTINGS' not in os.environ:
    config = 'settings.py'
    os.environ['LAVATAR_SETTINGS'] = os.path.abspath(config)

from gevent.pywsgi import WSGIServer
from lavatar import app


host = os.environ.get('APP_HOST', '127.0.0.1')
port = os.environ.get('APP_PORT', 5000)

http_server = WSGIServer((host, port), app)
http_server.serve_forever()
