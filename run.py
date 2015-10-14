#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from lavatar import app

app.run(host=os.environ.get('APP_HOST', 'localhost'),
        port=os.environ.get('APP_PORT', 5000))
