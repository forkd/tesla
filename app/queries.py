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


from app.models import db, Packet


def error_response(status):
    '''Auxiliary function to return JSON errors.'''
    if status == 404:
        return make_response(jsonify({'status':'not found'}), status)
    else:
        return make_response(jsonify({'status':'server error ({})'.format(
            status)}), status)

def get_packets(date_query=datetime.utcnow().strftime('%Y%m%d')):
    '''Main function to retrieve packets data.'''
    try:
        d = datetime.strptime(date_query, '%Y%m%d')
    except ValueError:
        if date_query == 'latest':
            d = datetime.utcnow().strftime('%Y%m%d')
        else:
            return error_response(404)
    packets = list()

    for p in Packet.query.filter_by(date=d):
        packets.append({'date':p.date, 'length':p.length, 
            'ip_src':p.ip_src, 'ip_src_geo':p.ip_src_geo, 
            'ip_dst':p.ip_dst, 'ip_dst_geo':p.ip_dst_geo, 
            'transport_proto':p.transport_proto,
            'transport_sport':p.transport_sport, 
            'transport_dport':p.transport_dport})
    
    if len(packets):
        return make_response(jsonify({'status':'OK', 'packets':packets}), 
            200)
    else:
        return error_response(404)

