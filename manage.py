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


import logging
from os import path, makedirs
from datetime import datetime, timedelta

from flask_script import Manager, Command
from sqlalchemy.exc import IntegrityError

from app import app
from app.config import Production


manager = Manager(app)
p = Production()  # configuration variables


if not path.isdir(p.BASE_DATA_PATH):
    makedirs(p.BASE_DATA_PATH)

logging.basicConfig(
    filename='{0}/{1}'.format(p.BASE_DATA_PATH, p.LOG_FILENAME),
    filemode='a',
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    level=logging.DEBUG)


@manager.command
def upd8db():
    from app.capture import PFLogger
    from app.getdata import pflog

    logging.info('Downloading new pflog file')
    try:
        pflog(p.BASE_DATA_PATH, p.PFLOG_FILENAME, p.BSD_CERT_PATH,
            p.BSD_USERNAME, p.BSD_ADDRESS, p.BSD_PFLOG_PATH)
    except Exception as e:
        logging.warning('Error downloading pflog: {}'.format(str(e)))
        return

    logging.info('Importing pflog to database')
    try:
        PFLogger('{0}/{1}'.format(p.BASE_DATA_PATH, p.PFLOG_FILENAME), 
            '{0}/{1}'.format(p.BASE_DATA_PATH, p.GEOLITE_FILENAME)).parser()
    except Exception as e:
        logging.warning('Error parsing pflog: {}'.format(str(e)))
        return

@manager.command
def upd8geo():
    from app.getdata import geolite
    logging.info('Updating GeoLite database')
    try:
        geolite(p.BASE_DATA_PATH, p.GEOLITE_FILENAME)
    except Exception as e:
        logging.warning('Error retrieving GeoLite: {}'.format(str(e)))
        return

@manager.command
def initdb():
    from app.models import db
    logging.info('Creating database')
    db.create_all()


if __name__ == '__main__':
    manager.run()

