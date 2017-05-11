#!/usr/bin/env python3
#queries.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''Tesla's database queries.'''

__author__ = 'José Lopes de Oliveira Jr.'


from datetime import datetime, timedelta

from flask import jsonify, make_response


from app.models import db, Capture, Summary


def error_response(status):
    '''Auxiliary function to return JSON errors.'''
    if status == 404:
        return make_response(jsonify({'status':'not found'}), status)
    else:
        return make_response(jsonify({'status':'server error ({})'.format(
            status)}), status)

def get_capture():
    '''Retrieves all packets in capture.'''
    capture = list()
    for c in Capture.query.all():
        capture.append({'date':c.date, 'length':c.length, 
            'ip_src':c.ip_src, 'ip_src_geo':c.ip_src_geo, 
            'ip_dst':c.ip_dst, 'ip_dst_geo':c.ip_dst_geo, 
            'transport_proto':c.transport_proto,
            'transport_sporc':c.transport_sport, 
            'transport_dport':c.transport_dport})
    if len(capture):
        return make_response(jsonify({'status':'OK', 'capture':capture}), 
            200)
    else:
        return error_response(404)

def get_summary(date):
    '''Retrieves the summary of date (format == AAAAMMYY).'''
    try:
        d = datetime.strptime(date, '%Y%m%d')
    except ValueError:
        d = db.session.query(db.func.max(Summary.date)).scalar()
    s = Summary.query.filter_by(date=d).scalar()
    if s:
        return make_response(jsonify({'status:':'OK',
            'summaries':[{'date':s.date, 'count':s.count, 'size':s.size, 
            'tcp':s.tcp, 'udp':s.udp}]}))
    else:
        return error_response(404)

