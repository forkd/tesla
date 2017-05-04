#!/usr/bin/env python3
#manage.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''Management routines for Tesla.'''

__author__ = 'José Lopes de Oliveira Jr.'


from flask_script import Manager, Command

from app import app


manager = Manager(app)


@manager.command
def upd8db():
    from app.pflog import PFLogger
    from app.getdata import pflog
    #TODO should have an exception handling here
    pflog()
    #TODO put these data into app/config.py
    PFLogger('app/data/pflog', 'app/data/geolite.mmdb').parser()

@manager.command
def upd8geo():
    from app.getdata import geolite
    geolite()

@manager.command
def initdb():
    from app.models import db
    db.create_all()


if __name__ == '__main__':
    manager.run()

