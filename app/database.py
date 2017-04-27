#!/usr/bin/env python3
#database.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''
Tesla's database initialization file.  It is in a
separate file to avoid circular imports.

'''

__author__ = 'José Lopes de Oliveira Jr.'


from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

