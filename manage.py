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
from app.config import Production


manager = Manager(app)


@manager.command
def upd8db():
    from app.pflog import PFLogger
    from app.getdata import pflog
    p = Production()
    #TODO should have an exception handling here
    #TODO pflog() should use config vars like PFLogger()
    pflog(p.BASE_DATA_PATH, p.PFLOG_FILENAME, p.BSD_CERT_PATH,
        p.BSD_USERNAME, p.BSD_ADDRESS, p.BSD_PFLOG_PATH)
    PFLogger('{0}/{1}'.format(p.BASE_DATA_PATH, p.PFLOG_FILENAME), 
        '{0}/{1}'.format(p.BASE_DATA_PATH, p.GEOLITE_FILENAME)).parser()

@manager.command
def upd8geo():
    from app.getdata import geolite
    p = Production()
    geolite(p.BASE_DATA_PATH, p.GEOLITE_FILENAME)

@manager.command
def initdb():
    from app.models import db
    db.create_all()


if __name__ == '__main__':
    manager.run()

