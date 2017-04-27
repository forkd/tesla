#!/usr/bin/env python3
#manage.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''Starts Tesla's web server and .'''

__author__ = 'José Lopes de Oliveira Jr.'


from flask_script import Manager, Command

from app import app


manager = Manager(app)


@manager.command
def initdb():
    from app.models import db
    db.create_all()

@manager.command
def upd8db():
    from app.pflog import PFLogger
    #TODO this should be parameters to make this
    # process scriptable.
    PFLogger('pflog.0', 'geolite.mmdb').parser()


if __name__ == '__main__':
    manager.run()

