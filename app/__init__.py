#!/usr/bin/env python3
#__init__.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''Tesla's configuration file.'''

__author__ = 'José Lopes de Oliveira Jr.'


from flask import Flask

from app.config import configure_app
from app.views import resp
from app.database import db

app = Flask('tesla')
configure_app(app)
app.register_blueprint(resp)
db.init_app(app)

