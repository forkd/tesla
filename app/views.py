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

from app.queries import get_capture, get_summary, get_topccsrc


resp = Blueprint('resp', __name__, template_folder='templates')


@resp.route('/')
def index():
    return render_template('index.html')

@resp.route('/capture')
@resp.route('/capture/<string:date>')
def route_capture(date='latest'):
    return get_capture(date)

@resp.route('/summary')
@resp.route('/summary/<string:date>')
def route_summary(date='latest'):
    return  get_summary(date)

@resp.route('/topccsrc')
@resp.route('/topccsrc/<string:date>')
def route_topccsrc(date='latest'):
    return get_topccsrc(date)

