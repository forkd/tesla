#!/usr/bin/env python3
#capture.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''Parses a pflog file and write it into a database.'''

__author__ = 'José Lopes de Oliveira Jr.'


from datetime import datetime

import pyshark
import geoip2.database
from geoip2.errors import AddressNotFoundError

from app.models import db, Capture


class PFLogger:
    '''
    Opens and parses pflog files adding geographical information.

    Args:
        p (string): pflog file name --default: app/data/pflog
        g (string): GeoLite database path --default: app/data/geolite.mmdb

    Writes all data into a database defined in app.models.db.

    '''

    def __init__(self, p, g):
        self.capture = pyshark.FileCapture(p)
        self.geo = geoip2.database.Reader(g)

    def parser(self):
        counter = 0
        for c in self.capture:
            # ip layer
            try:
                ip_layer = [c['ip'].src,
                    self.geo.country(c['ip'].src).country.iso_code,
                    c['ip'].dst,
                    self.geo.country(c['ip'].dst).country.iso_code,
                    c['ip'].version, c['ip'].ttl]
            except AddressNotFoundError:
            #TODO check which addr has no geolocation and record the other
                ip_layer = [c['ip'].src, None, c['ip'].dst, None,
                    c['ip'].version, c['ip'].ttl]
            except KeyError:
                ip_layer = [None, None, None, None, None, None]

            # icmp layer
            try:
                icmp_layer = [c['icmp'].type, c['icmp'].code]
            except KeyError:
                icmp_layer = [None, None]

            # tcp layer
            try:
                tcp_layer = [c['tcp'].srcport, c['tcp'].dstport,
                    int(c['tcp'].flags,16)]
                udp_layer = [None, None]
            except KeyError:
                tcp_layer = [None, None, None]
                try:
                    udp_layer = [c['udp'].srcport, c['udp'].dstport]
                except KeyError:
                    udp_layer = [None, None]

            db.session.add(Capture(datetime.utcfromtimestamp(float(
                c.sniff_timestamp)), 
                c.captured_length,
                ip_layer[0], ip_layer[1], ip_layer[2], ip_layer[3],
                ip_layer[4], ip_layer[5],
                icmp_layer[0], icmp_layer[1],
                tcp_layer[0], tcp_layer[1], tcp_layer[2],
                udp_layer[0], udp_layer[1]))
                
            # Less commits, better performance.
            # In fact, it's not quite right, because using 20000 
            # disk usage was diminished and CPU improved, but 
            # there were no expressive gains above this value.
            counter += 1
            if counter == 20000:
                db.session.commit()
                counter = 0
        db.session.commit()  # last items guaranteed

