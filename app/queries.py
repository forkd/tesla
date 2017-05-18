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

from app.models import db, Capture


def error_response(status):
    '''Auxiliary function to return JSON errors.'''
    if status == 404:
        return make_response(jsonify({'status':'not found'}), status)
    else:
        return make_response(jsonify({'status':'server error ({})'.format(
            status)}), status)

def get_capture(date):
    '''Retrieves all packets in capture.'''
    try:
        d = datetime.strptime(date, '%Y%m%d')
        d = d.replace(hour=23, minute=59, second=59, microsecond=99999)
    except ValueError:
        d = db.session.query(db.func.max(Capture.date)).scalar()
    min_d = d.replace(hour=0, minute=0, second=0, microsecond=0)

    capture = list()
    for c in db.session.query(Capture).filter(min_d <= Capture.date,
        Capture.date <= d):
        capture.append({'date':c.date, 'length':c.length, 
            'ip_src':c.ip_src, 'ip_src_geo':c.ip_src_geo, 
            'ip_dst':c.ip_dst, 'ip_dst_geo':c.ip_dst_geo, 
            'ip_version':c.ip_version, 'ip_ttl':c.ip_ttl,
            'icmp_type':c.icmp_type, 'icmp_code':c.icmp_code,
            'tcp_sport':c.tcp_sport, 'tcp_dport':c.tcp_dport, 
            'tcp_flags':c.tcp_flags,
            'udp_sport':c.udp_sport, 'udp_dport':c.udp_dport})
    if len(capture):
        return make_response(jsonify({'status':'OK', 'capture':capture}), 
            200)
    else:
        return error_response(404)

def get_summary(date):
    '''Retrieves the summary of date (format == AAAAMMYY).'''
    try:
        d = datetime.strptime(date, '%Y%m%d')
        d = d.replace(hour=23, minute=59, second=59, microsecond=99999)
    except ValueError:
        d = db.session.query(db.func.max(Capture.date)).scalar()
    min_d = d.replace(hour=0, minute=0, second=0, microsecond=0)

    size = db.session.query(db.func.sum(Capture.length)).\
        filter(Capture.date >= min_d, Capture.date <= d).scalar()

    if size is None:
        return error_response(404)

    count = db.session.query(db.func.count(Capture.date)).\
        filter(Capture.date >= min_d, Capture.date <= d).scalar()
    tcp = db.session.query(db.func.count(Capture.date)).\
        filter(Capture.tcp_sport != None).\
        filter(Capture.date >= min_d, Capture.date <= d).scalar()
    udp = db.session.query(db.func.count(Capture.date)).\
        filter(Capture.udp_sport != None).\
        filter(Capture.date >= min_d, Capture.date <= d).scalar()
    icmp = db.session.query(db.func.count(Capture.date)).\
        filter(Capture.icmp_type != None).\
        filter(Capture.date >= min_d, Capture.date <= d).scalar()

    return make_response(jsonify({'status:':'OK',
        'summaries':[{'date':d, 'count':count, 'size':size, 
        'tcp':tcp, 'udp':udp, 'icmp':icmp}]}), 200)

def get_topccsrc(date):
    '''Retrieves the top countries in date (format == AAAAMMYY).'''
    try:
        d = datetime.strptime(date, '%Y%m%d')
        d = d.replace(hour=23, minute=59, second=59, microsecond=99999)
    except ValueError:
        d = db.session.query(db.func.max(Capture.date)).scalar()
    min_d = d.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # put here the ip addrs you don't want to include in the results
    exclude_ips = []

    cc = dict(db.session.query(Capture.ip_src_geo, 
        db.func.count(Capture.ip_src_geo).label('count')).\
        filter(Capture.date >= min_d, Capture.date <= d).\
        filter(Capture.ip_src.notin_(exclude_ips)).\
        group_by(Capture.ip_src_geo).all())
    
    if not cc:
        return error_response(404)

    cc['date'] = d
    try:  # jsonify breaks with None items in dict
        if cc[None]:
            cc['None'] = cc.pop(None)
        else:
            cc.pop(None)
    except KeyError:
        pass

    return make_response(jsonify({'status':'OK', 'topcc':[cc]}), 200)

