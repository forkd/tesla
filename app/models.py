#!/usr/bin/env python3
#models.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''Tesla's database models.'''

__author__ = 'José Lopes de Oliveira Jr.'


from datetime import datetime

from app.database import db


class Capture(db.Model):
    __tablename__ = 'Captures'
    date = db.Column(db.DateTime, primary_key=True)
    length = db.Column(db.Integer)
    ip_src = db.Column(db.String(128))
    ip_src_geo = db.Column(db.String(2))
    ip_dst = db.Column(db.String(128))
    ip_dst_geo = db.Column(db.String(2))
    ip_version = db.Column(db.Integer)
    ip_ttl = db.Column(db.Integer)
    icmp_type = db.Column(db.Integer)
    icmp_code = db.Column(db.Integer)
    tcp_sport = db.Column(db.Integer)
    tcp_dport = db.Column(db.Integer)
    tcp_flags = db.Column(db.Integer)
    udp_sport = db.Column(db.Integer)
    udp_dport = db.Column(db.Integer)

    def __init__(self, d, l, ips, ipsg, ipd, ipdg, ipver, ipttl, itp, ico,
        tsp, tdp, tf, usp, udp):
        self.date = d
        self.length = l
        self.ip_src = ips
        self.ip_src_geo = ipsg
        self.ip_dst = ipd
        self.ip_dst_geo = ipdg
        self.ip_version = ipver
        self.ip_ttl = ipttl
        self.icmp_type = itp
        self.icmp_code = ico
        self.tcp_sport = tsp
        self.tcp_dport = tdp
        self.tcp_flags = tf
        self.udp_sport = usp
        self.udp_dport = udp

    def __repr__(self):
        return '<Packet lenght: {}>'.format(self.length)

