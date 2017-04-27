#!/usr/bin/env python3
#views.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''Routing rules for Tesla.'''

__author__ = 'José Lopes de Oliveira Jr.'


from flask import Blueprint, render_template

from app.queries import get_packets


resp = Blueprint('resp', __name__, template_folder='templates')


@resp.route('/')
def index():
    return render_template('index.html')

@resp.route('/packets/')
@resp.route('/packets/<int:days>')
def route_packets(days=1):
    return get_packets(days)

