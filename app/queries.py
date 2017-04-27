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
    if status == 404:
        return make_response(jsonify({'status': 'not found'}), status)
    else:
        return make_response(jsonify({'status': 'server error ({})'.format(
            status)}), status)

def packet_response(status, d, l, ips, ipsg, ipd, ipdg, tp, tsp, tdp):
    if status == 200:
        return {'date':d, 'length':l, 'ip_src':ips, 'ip_src_geo':ipsg, 
            'ip_dst':ipd, 'ip_dst_geo':ipdg, 'transport_proto':tp,
            'transport_sport':tsp, 'transport_dport':tdp}
    else:
        return error_response(status)

def get_packets(d):
    end = db.session.query(db.func.max(Packet.date)).scalar()
    begin = end - timedelta(days=d)
    packets = list()
    
    for p in Packet.query.filter(begin<=end):
        packets.append(packet_response(200, p.date, p.length,
            p.ip_src, p.ip_src_geo, p.ip_dst, p.ip_dst_geo,
            p.transport_proto, p.transport_sport, p. transport_dport))

    if len(packets):
        return jsonify({'status':'OK', 'packets':packets})
    else:
        return packet_response(404)

