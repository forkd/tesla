#!/usr/bin/env python3
#config.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''Tesla configuration file. '''

__author__ = 'José Lopes de Oliveira Jr.'


import os


class Production:
    DEBUG = False
    JSON_AS_ASCII = False
    DBUSER = 'postgres'
    DBPASS = 'foobar'
    DBHOST = '127.0.0.1'
    DBPORT = '5432'
    DBNAME = 'tesla'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{0}:{1}@{2}:{3}\
        /{4}'.format(DBUSER, DBPASS, DBHOST, DBPORT, DBNAME)
    SECRET_KEY = 'Q.\=wNpSa=J}1>9bH*VPyYgWf1[<R[%*0NJ-?jJ"H*g"|S=aP]]'

    BASE_DATA_PATH = 'app/data'
    PFLOG_FILENAME = 'pflog'
    GEOLITE_FILENAME = 'geolite.mmdb'
    LOG_FILENAME = 'tesla.log'

    BSD_CERT_PATH = 'ssh-private-key-path'
    BSD_USERNAME = 'username'
    BSD_ADDRESS = 'ip-addr-or-hostname'
    BSD_PFLOG_PATH = '/var/log/pf/pflog.0'

class Development(Production):
    DEBUG = True


config = {
    'development': 'app.config.Development',
    'production': 'app.config.Production'
}


def configure_app(app):
    app.config.from_object(config[os.getenv('TESLA_MODE', 'production')])



